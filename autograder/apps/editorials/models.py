from django.db import models
from autograder.apps.contests.models import Contest
from autograder.apps.problems.models import Problem

class Editorial(models.Model):
    contest = models.OneToOneField(Contest, on_delete=models.CASCADE, related_name="contest_editorial")

    def __str__(self):
        return f"Editorial C#{self.contest.id}"

class EditorialEntry(models.Model):
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, related_name="entries")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField(blank=True)
    problem_text = models.TextField(blank=True)

    class Meta:
        unique_together = ("editorial", "problem")

    def __str__(self):
        return f"Editorial Entry: P#{self.problem.id} in C#{self.editorial.contest.id}"
