from django.db import models

class RatingChange(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(
        'index.GraderUser',
        on_delete=models.CASCADE,
        db_column='username'
    )
    rating = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"RatingChange #{self.id} for User {self.userid_id} -> {self.rating}"
