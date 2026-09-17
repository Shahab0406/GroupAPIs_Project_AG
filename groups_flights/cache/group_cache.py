from django.conf import settings
from django.core.cache import cache

GROUP_CACHE_KEY_PREFIX = "group"


class GroupCache:
    @staticmethod
    def cache_key(group_id: int) -> str:
        return f"{GROUP_CACHE_KEY_PREFIX}:{group_id}"

    @classmethod
    def timeout(cls) -> int:
        return getattr(settings, "GROUP_CACHE_TIMEOUT", 60 * 60 * 24)

    @classmethod
    def get(cls, group_id: int) -> dict | None:
        return cache.get(cls.cache_key(group_id))

    @classmethod
    def set(cls, group_id: int, group_data: dict) -> None:
        cache.set(cls.cache_key(group_id), group_data, timeout=cls.timeout())

    @classmethod
    def delete(cls, group_id: int) -> None:
        cache.delete(cls.cache_key(group_id))
