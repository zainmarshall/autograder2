from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Problem
from .tasks import add_problem_to_coderunner_task, add_tests_to_coderunner_task
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Problem)
def add_problem_folder(sender, instance, created, **kwargs):
    add_problem_to_coderunner_task.delay(instance.id)


@receiver(post_save, sender=Problem)
def add_problem_tests(sender, instance, created, **kwargs):
    add_tests_to_coderunner_task.delay(instance.id)
