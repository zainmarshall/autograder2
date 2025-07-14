import asyncio
import aiohttp
import logging
from typing import Dict, Any
from urllib.parse import urlencode

from django.conf import settings
from django.db import transaction

from .models import Submission

logger = logging.getLogger(__name__)

class SubmissionQueue:
    """
    Manages an asynchronous queue for grading programming submissions.
    """
    def __init__(self):
        self._tasks: asyncio.Queue = asyncio.Queue()
        self._runner_task: asyncio.Task | None = None
        self._paused: bool = False
        self._currently_processing: int | None = None

    def _start_runner_if_needed(self):
        """Starts the runner task if it's not already running."""
        if not self._runner_task or self._runner_task.done():
            self._runner_task = asyncio.create_task(self._run())
            self._runner_task.add_done_callback(self._handle_runner_completion)
            logger.info("Submission queue runner has been started.")

    def _handle_runner_completion(self, task: asyncio.Task):
        """Callback to handle exceptions if the runner task crashes."""
        try:
            task.result()
        except Exception as e:
            logger.exception(f"Submission runner task failed unexpectedly: {e}")
        logger.info("Submission queue runner has stopped.")

    async def _run(self):
        """The main loop that processes submissions from the queue."""
        while not self._paused:
            try:
                # Wait for the next submission indefinitely until the queue is paused
                submission_id = await self._tasks.get()
                self._currently_processing = submission_id
                
                logger.info(f"Processing submission ID: {submission_id}")
                await self._grade_submission(submission_id)
                
                self._tasks.task_done()
                self._currently_processing = None

            except asyncio.CancelledError:
                logger.info("Runner task was cancelled.")
                break
            except Exception as e:
                logger.exception(f"An error occurred while processing submission ID {self._currently_processing}: {e}")
                if self._currently_processing:
                    await self._mark_submission_as_error(
                        self._currently_processing,
                        f"A critical error occurred in the grading queue: {str(e)}"
                    )
                # Continue to the next task
                continue

    async def _grade_submission(self, submission_id: int):
        """Fetches submission details and sends them to the code runner."""
        try:
            # Use select_related to efficiently fetch the related problem
            submission = await Submission.objects.select_related('problem').aget(id=submission_id)
            problem = submission.problem
        except Submission.DoesNotExist:
            logger.error(f"Submission {submission_id} not found for grading.")
            return

        coderunner_url = settings.CODERUNNER_URL # Recommended: Store URL in settings.py

        payload = {
            "lang": submission.language,
            "problemid": str(problem.id),
            "code": submission.code,
            "tl": problem.tl,
            "ml": problem.ml
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    coderunner_url,
                    data=urlencode(payload),
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                ) as response:
                    response.raise_for_status() # Raises an exception for 4xx/5xx responses
                    data = await response.json()
                    
                    logger.info(f"Response from coderunner for submission {submission_id}: {data}")
                    
                    # Update submission in a transaction to ensure data integrity
                    await self.update_submission_from_result(submission, data)

        except aiohttp.ClientError as e:
            logger.error(f"Network error while communicating with coderunner: {e}")
            await self._mark_submission_as_error(submission_id, f"Could not connect to the grading service: {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred during grading for submission {submission_id}.")
            await self._mark_submission_as_error(submission_id, f"An unexpected grading server error occurred: {e}")
            
    @staticmethod
    @transaction.atomic
    async def update_submission_from_result(submission: Submission, result_data: Dict[str, Any]):
        """Atomically updates submission fields from coderunner result."""
        submission.verdict = result_data.get("verdict", "ER") # ER for "Error"
        submission.runtime = result_data.get("runtime", -1)
        submission.memory = result_data.get("memory", -1)
        submission.insight = result_data.get("output", "")
        await submission.asave()

    async def _mark_submission_as_error(self, submission_id: int, error_message: str):
        """Marks a submission with a system error verdict."""
        try:
            async with transaction.atomic():
                submission = await Submission.objects.aget(id=submission_id)
                submission.verdict = "ERROR"
                submission.insight = error_message
                await submission.asave()
        except Submission.DoesNotExist:
            logger.error(f"Could not find submission {submission_id} to mark as an error.")
        except Exception as e:
            logger.error(f"Failed to save error state for submission {submission_id}: {e}")

    # --- Public Control Methods ---
    
    async def add_to_queue(self, submission_id: int):
        """Adds a new submission to the grading queue."""
        await self._tasks.put(submission_id)
        logger.info(f"Submission {submission_id} added to the queue.")
        self._start_runner_if_needed()

    def get_queue_status(self) -> Dict[str, Any]:
        """Returns the current state of the queue."""
        queued_ids = [item for item in self._tasks._queue]
        return {
            "is_running": self._runner_task is not None and not self._runner_task.done(),
            "is_paused": self._paused,
            "queue_length": self._tasks.qsize(),
            "currently_processing": self._currently_processing,
            "queued_ids": queued_ids
        }

    def toggle_pause(self, pause: bool):
        """Pauses or resumes the queue processing."""
        if self._paused == pause:
            return # No change
            
        self._paused = pause
        logger.info(f"Submission queue has been {'paused' if pause else 'resumed'}.")
        
        if not pause:
            # If resuming, ensure the runner is started
            self._start_runner_if_needed()
        elif self._runner_task and not self._runner_task.done():
            # If pausing, we can optionally cancel the current runner
            # This will stop it after the current submission is finished
            pass # The loop in _run() will naturally exit on the next iteration check

    async def skip_submission(self, submission_id: int):
        """Removes a submission from the queue and marks it as skipped."""
        # This is a simplified way to "remove" from asyncio.Queue.
        # A more robust implementation might require a different data structure
        # if frequent removal from the middle of the queue is needed.
        new_queue = asyncio.Queue()
        found = False
        while not self._tasks.empty():
            item = await self._tasks.get()
            if item == submission_id:
                found = True
                continue
            await new_queue.put(item)
        
        self._tasks = new_queue

        if found:
            try:
                async with transaction.atomic():
                    submission = await Submission.objects.aget(id=submission_id)
                    submission.verdict = "SKIPPED"
                    submission.insight = "This submission was manually skipped by an admin."
                    await submission.asave()
                logger.info(f"Submission {submission_id} was skipped by an admin.")
            except Submission.DoesNotExist:
                logger.error(f"Attempted to skip non-existent submission {submission_id}")
        return found


# --- Singleton Instance ---
# This acts like a global instance but is managed cleanly.
# This code will run once when Django loads the module.
submission_queue = SubmissionQueue()