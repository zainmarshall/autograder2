import random
from datetime import timedelta
from django.utils import timezone
from autograder.apps.index.models import GraderUser
from autograder.apps.contests.models import Contest
from autograder.apps.problems.models import Problem
from autograder.apps.runtests.models import Submission  # Adjust this if Submission is in a different app

# Fetch some existing users, contests, and problems
users = list(GraderUser.objects.all())
contests = list(Contest.objects.all())
problems = list(Problem.objects.all())

# Simple safety check
if not users or not contests or not problems:
    raise Exception("Ensure at least one GraderUser, Contest, and Problem exist in the database.")

languages = ['cpp', 'java', 'python']
verdicts = ['AC']

for i in range(500):
    Submission.objects.create(
        language=random.choice(languages),
        code=f'// Sample code snippet {i}\nprint("Hello, World!")',
        usr=random.choice(users),
        verdict=random.choice(verdicts),
        runtime=random.randint(1, 5000),  # milliseconds
        memory=random.randint(1000, 50000),  # kilobytes
        contest=random.choice(contests),
        problem=random.choice(problems),
        insight="insight here",
        timestamp=timezone.now() - timedelta(minutes=random.randint(0, 10000))
    )

print("500 filler submissions created.")
