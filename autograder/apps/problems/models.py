from django.db import models


class Problem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contest = models.ForeignKey("contests.Contest", on_delete=models.CASCADE)
    points = models.IntegerField()

    statement = models.TextField()
    inputtxt = models.TextField()
    outputtxt = models.TextField()
    samples = models.TextField()

    tl = models.IntegerField(null=True, blank=True)
    ml = models.IntegerField(null=True, blank=True)

    interactive = models.BooleanField(default=False)
    secret = models.BooleanField(default=False)

    testcases_zip = models.FileField(upload_to="problem_testcases/", blank=True)

    has_simulation = models.BooleanField(default=False)
    simulation_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
