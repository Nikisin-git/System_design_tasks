import os
import json

from app.cache import redis_client
from app.models import User


class UserCacheService:

    @staticmethod
    def _user_cache_key(login: str) -> str:
        return f"user:{login}"

    @staticmethod
    def _search_cache_key(first_name: str, last_name: str) -> str:
        return f"user_search:{first_name}:{last_name}"

    @classmethod
    async def get_user_by_login(cls, login: str):
        key = cls._user_cache_key(login)
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    @classmethod
    async def set_user_by_login(cls, user: User):
        key = cls._user_cache_key(user.login)
        user_data = {
            "id": user.id,
            "full_name": user.full_name,
            "login": user.login,
        }
        await redis_client.set(key, json.dumps(user_data), ex=3600)  # TTL 1 час

    @classmethod
    async def delete_user_by_login(cls, login: str):
        key = cls._user_cache_key(login)
        await redis_client.delete(key)

    @classmethod
    async def get_search_users(cls, first_name: str, last_name: str):
        key = cls._search_cache_key(first_name, last_name)
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    @classmethod
    async def set_search_users(cls, first_name: str, last_name: str, users: list):
        key = cls._search_cache_key(first_name, last_name)
        await redis_client.set(key, json.dumps(users), ex=3600)  # TTL 1 час

    @classmethod
    async def delete_search_cache(cls, first_name: str, last_name: str):
        key = cls._search_cache_key(first_name, last_name)
        await redis_client.delete(key)