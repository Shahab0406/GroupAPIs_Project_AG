from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from groups_flights.cache import GroupCache
from groups_flights.models import Group

GROUP_PRICE_FIELDS = {
    "buying_currency",
    "buying_price_per_seat_adult",
    "buying_price_per_seat_child",
    "buying_price_per_seat_infant",
    "selling_currency",
    "selling_price_per_seat_adult",
    "selling_price_per_seat_child",
    "selling_price_per_seat_infant",
    "token_amount",
}
GROUP_SEAT_FIELDS = {
    "adult_seats",
    "child_seats",
}
GROUP_CACHE_INVALIDATE_FIELDS = GROUP_PRICE_FIELDS | GROUP_SEAT_FIELDS


def _should_invalidate_cache(instance: Group) -> bool:
    if instance.pk is None:
        return False

    previous = (
        Group.objects.filter(pk=instance.pk)
        .values(*GROUP_CACHE_INVALIDATE_FIELDS)
        .first()
    )
    if not previous:
        return False

    return any(
        previous[field] != getattr(instance, field)
        for field in GROUP_CACHE_INVALIDATE_FIELDS
    )


@receiver(pre_save, sender=Group)
def mark_group_cache_invalidation(sender, instance: Group, **kwargs):
    instance._invalidate_group_cache = _should_invalidate_cache(instance)


@receiver(post_save, sender=Group)
def invalidate_group_cache(sender, instance: Group, **kwargs):
    if getattr(instance, "_invalidate_group_cache", False):
        GroupCache.delete(instance.pk)
