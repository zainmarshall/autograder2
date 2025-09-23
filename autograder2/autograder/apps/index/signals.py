from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GraderUser
from decimal import Decimal
from ..rankings.utils import get_codeforces_rating
import threading
import logging

logger = logging.getLogger(__name__)
_signal_lock = threading.local()


@receiver(post_save, sender=GraderUser)
def update_rating(sender, instance, created, **kwargs):
    if getattr(_signal_lock, "in_signal", False):
        return

    usaco_map = {
        "Not Participated": 800,
        "Bronze": 800,
        "Silver": 1200,
        "Gold": 1600,
        "Platinum": 1900,
    }

    new_usaco_rating = usaco_map.get(instance.usaco_division, 800)
    new_cf_rating = get_codeforces_rating(instance)
    if new_cf_rating is None:
        new_cf_rating = instance.cf_rating
    vals = [new_usaco_rating, new_cf_rating, instance.inhouse]
    vals.sort()
    new_index = (
        Decimal("0.2") * vals[0] + Decimal("0.35") * vals[1] + Decimal("0.45") * vals[2]
    )

    fields_to_update = []
    if instance.usaco_rating != new_usaco_rating:
        instance.usaco_rating = new_usaco_rating
        fields_to_update.append("usaco_rating")

    if instance.cf_rating != new_cf_rating:
        instance.cf_rating = new_cf_rating
        fields_to_update.append("cf_rating")

    if instance.index != new_index:
        instance.index = new_index
        fields_to_update.append("index")

    if fields_to_update:
        try:
            _signal_lock.in_signal = True
            instance.save(update_fields=fields_to_update)
        finally:
            _signal_lock.in_signal = False
