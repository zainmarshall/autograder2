import os
import logging
import requests
import zipfile
import tempfile
from urllib.parse import urlencode
from celery import shared_task
from django.conf import settings
from ..problems.models import Problem

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def add_problem_to_coderunner_task(self, problem_id: int):
    logger.info(f"Registering problem {problem_id} with the coderunner.")
    coderunner_url = settings.CODERUNNER_URL + "addProblem"
    try:
        response = requests.post(
            coderunner_url,
            data=urlencode({"pid": problem_id}),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        logger.info(f"Successfully added problem {problem_id} to coderunner.")
    except requests.exceptions.RequestException as exc:
        logger.warning(f"Network error for problem {problem_id}: {exc}. Retrying...")
        raise self.retry(exc=exc)
    except Exception:
        logger.exception(
            f"An unexpected error occurred while adding problem {problem_id}."
        )
        raise


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def add_tests_to_coderunner_task(self, problem_id: int):
    logger.info(f"Starting test case upload for problem {problem_id}.")
    try:
        problem = Problem.objects.get(id=problem_id)
        if not problem.testcases_zip or not hasattr(problem.testcases_zip, "path"):
            logger.warning(f"No zip file found for problem {problem_id}.")
            return

        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(problem.testcases_zip.path, "r") as zip_ref:
                zip_ref.extractall(tmpdir)
                names = zip_ref.namelist()

            upload_url = settings.CODERUNNER_URL + "addTest"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            testcases = {}

            for name in names:
                full_path = os.path.join(tmpdir, name)
                if not os.path.isfile(full_path):
                    continue

                base, ext = os.path.splitext(name)
                if not base.isdigit() or ext not in [".in", ".out"]:
                    logger.error(f"Invalid file name: {name}")
                    return

                tid = int(base)
                if tid not in testcases:
                    testcases[tid] = {}
                with open(full_path, "r") as f:
                    content = f.read()
                    if ext == ".in":
                        testcases[tid]["test"] = content
                    else:
                        testcases[tid]["out"] = content

            for tid, tc in testcases.items():
                payload = {
                    "pid": problem_id,
                    "tid": tid,
                    "test": tc["test"],
                    "out": tc["out"],
                }
                response = requests.post(
                    upload_url, data=urlencode(payload), headers=headers
                )
                if response.status_code != 200:
                    logger.error(
                        f"Failed to upload test {tid} for problem {problem_id}: {response.text}"
                    )
                else:
                    logger.info(f"Uploaded test {tid} for problem {problem_id}")

    except Problem.DoesNotExist:
        logger.error(f"Problem {problem_id} not found for test upload.")
    except requests.exceptions.RequestException as exc:
        logger.warning(
            f"Network error during test upload for {problem_id}: {exc}. Retrying..."
        )
        raise self.retry(exc=exc)
    except Exception:
        logger.exception(
            f"An unexpected error occurred during test upload for {problem_id}."
        )
        raise
