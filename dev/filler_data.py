import os
import django
import random
import datetime
from datetime import timedelta
from faker import Faker
from django.utils import timezone


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autograder.settings')
django.setup()

from autograder.apps.index.models import GraderUser  # noqa: E402
from autograder.apps.contests.models import Contest  # noqa: E402
from autograder.apps.problems.models import Problem  # noqa: E402
from autograder.apps.runtests.models import Submission # noqa: E402


fake = Faker()

def create_users():
    users = []
    for i in range(20):
        user = GraderUser.objects.create_user(
            email="example@example.com",
            password="password123",
            username=f"user{i}",
            display_name="User User",
            cf_handle=random.choice(['tourist', 'jiangly', 'orzdevinwang', 'ksun48']),
            grade=random.choice(['9', '10', '11', '12']),
            usaco_division=random.choice(list(GraderUser.USACO_DIVISIONS.keys())),
        )
        users.append(user)

    for i in range(20, 25):
        admin = GraderUser.objects.create_superuser(
            email="example@example.com",
            password="adminpass",
            username=f"admin{i}",
            display_name="Admin Admin",
            cf_handle=random.choice(['tourist', 'jiangly', 'orzdevinwang', 'ksun48']),
            grade=random.choice(['9', '10', '11', '12']),
            usaco_division=random.choice(list(GraderUser.USACO_DIVISIONS.keys())),
        )
        users.append(admin)

    return users

def create_contests():
    contests = []
    now = timezone.now()
    for i in range(5):
        start_time = now - timedelta(days=random.randint(30, 365))
        end_time = start_time + timedelta(hours=2)
        contest = Contest.objects.create(
            name=f"Contest {i}",
            rated=True,
            season=2025,
            tjioi=(False if i < 4 else True),
            start=start_time,
            end=end_time,
            editorial=fake.text(max_nb_chars=15)
        )
        contests.append(contest)
    return contests

def create_problems_and_submissions(users, contests):
    problems = []

    for contest in contests:
        # Create 5 problems for each contest
        for i in range(5):
            problem = Problem.objects.create(
                name=f"Problem {chr(65 + i)}",
                contest=contest,
                points=(i + 1)*100,
                statement="statement here",
                solution="solution here",
                inputtxt="input.txt content",
                outputtxt="output.txt content",
                samples="Sample input/output",
                tl=1000,
                ml=256,
                interactive=False,
                secret=False,
            )
            problems.append(problem)

        for user in users:
            for problem in Problem.objects.filter(contest=contest):
                if random.random() < 0.75:
                    start = contest.start
                    end = contest.end
                    delta = (end - start).total_seconds()
                    random_seconds = random.uniform(0, delta)
                    timestamp = start + datetime.timedelta(seconds=random_seconds)

                    Submission.objects.create(
                        language=random.choice(["Python", "C++", "Java"]),
                        code=fake.text(max_nb_chars=200),
                        usr=user,
                        verdict=random.choice(["AC", "Wrong Answer"]),
                        runtime=random.randint(10, 2000),
                        memory=random.randint(10000, 100000),
                        contest=contest,
                        problem=problem,
                        insight="insight here",
                        timestamp=timestamp,
                    )

    return problems


if __name__ == "__main__":
    users = create_users()
    contests = create_contests()
    problems = create_problems_and_submissions(users, contests)
    print("Filler data created successfully.")
