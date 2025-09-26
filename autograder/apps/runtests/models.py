from django.db import models
from django.utils import timezone


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=10)
    code = models.TextField()
    usr = models.ForeignKey("index.GraderUser", on_delete=models.CASCADE)
    verdict = models.TextField(default="Waiting in Queue")
    runtime = models.IntegerField(default=-1)
    contest = models.ForeignKey("contests.Contest", on_delete=models.CASCADE)
    problem = models.ForeignKey("problems.Problem", on_delete=models.CASCADE)
    insight = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=True)

    class Meta:
        get_latest_by = "timestamp"

    def __str__(self):
        return f"Submission #{self.id} by user {self.usr}"
