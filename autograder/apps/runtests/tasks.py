import logging
import requests
from typing import Dict, Any
from urllib.parse import urlencode

from celery import shared_task
from django.conf import settings
from django.db import transaction

from .models import Submission

logger = logging.getLogger(__name__)


@transaction.atomic
def _update_submission_from_result(submission_id: int, result_data: Dict[str, Any]):
    submission = Submission.objects.select_for_update().get(id=submission_id)
    submission.verdict = result_data.get("verdict", "ER")
    submission.runtime = result_data.get("runtime", -1)
    submission.memory = result_data.get("memory", -1)
    submission.insight = result_data.get("output", "")
    submission.save()


@transaction.atomic
def _mark_submission_as_error(submission_id: int, error_message: str):
    try:
        submission = Submission.objects.select_for_update().get(id=submission_id)
        submission.verdict = "Internal Server Error"
        submission.insight = error_message
        submission.save()
    except Submission.DoesNotExist:
        logger.error(f"Could not find submission {submission_id} to mark as an error.")


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def grade_submission_task(self, submission_id: int):
    try:
        submission = Submission.objects.select_related("problem").get(id=submission_id)
        if submission.verdict == "Skipped":
            logger.info(
                f"Submission {submission_id} is marked as 'Skipped'. Aborting task."
            )
            return

    except Submission.DoesNotExist:
        logger.error(f"Submission {submission_id} not found. Task will not be retried.")
        return

    coderunner_url = settings.CODERUNNER_URL + "run"
    payload = {
        "lang": submission.language,
        "problemid": str(submission.problem.id),
        "tl_string": str(submission.problem.tl),
        "ml_string": str(submission.problem.ml),
        "code": submission.code,
    }

    try:
        response = requests.post(
            coderunner_url,
            data=urlencode(payload),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()

        _update_submission_from_result(submission_id, response.json())
        logger.info(f"Successfully graded submission {submission_id}.")

    except requests.exceptions.RequestException as exc:
        if response is not None and response.status_code == 400:
            try:
                error_message = response.json().get("error", response.text)
            except Exception:
                error_message = response.text
            logger.warning(
            f"Bad request for submission {submission_id}: {error_message}"
            )
            _mark_submission_as_error(submission_id, error_message)
        else:
            logger.warning(f"Network error for submission {submission_id}: {exc}. Retrying...")
            _mark_submission_as_error(submission_id, "Could not connect to the grading service.")
        raise self.retry(exc=exc)

    except Exception as exc:
        logger.exception(
            f"An unexpected error occurred for submission {submission_id}."
        )
        _mark_submission_as_error(
            submission_id, f"An unexpected error occurred: {str(exc)}"
        )
