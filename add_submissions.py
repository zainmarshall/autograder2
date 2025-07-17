import asyncio
import os
import django
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autograder.settings")
django.setup()

from autograder.apps.index.models import GraderUser  # noqa: E402
from autograder.apps.problems.models import Problem  # noqa: E402
from autograder.apps.runtests.models import Submission  # noqa: E402
from django.shortcuts import get_object_or_404  # noqa: E402
from autograder.apps.runtests.utils import submission_queue  # noqa: E402


async def add_subs():

    for _ in range(100):
        grader_user = await sync_to_async(get_object_or_404)(GraderUser, id=27)
        problem_obj = await sync_to_async(Problem.objects.select_related('contest').get)(id=1)
        contest_obj = problem_obj.contest
        with open("sol.py", "r", encoding="utf-8") as f:
            code_str = f.read()
        code_bytes = code_str
        new_sub = await sync_to_async(Submission.objects.create)(
            usr=grader_user,
            code=code_bytes,
            problem=problem_obj,
            language="py",
            contest=contest_obj,
        )
        await sync_to_async(new_sub.save)()
        await submission_queue.add_to_queue(new_sub.id)


asyncio.run(add_subs())