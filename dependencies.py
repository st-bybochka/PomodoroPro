from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from repository import TaskRepository, CategoryRepository, TaskCache, UserRepository
from cache import get_redis_connection
from service import TaskService, UserService, AuthService


async def get_task_repository(
        session: AsyncSession = Depends(get_async_session)
) -> TaskRepository:
    return TaskRepository(session)


async def get_category_repository(
        session: AsyncSession = Depends(get_async_session)
) -> CategoryRepository:
    return CategoryRepository(session)


async def get_cache_task_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


async def get_task_service(
        task_repository: TaskRepository = Depends(get_task_repository),
        task_cache: TaskCache = Depends(get_cache_task_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )


async def get_user_repository(
        session: AsyncSession = Depends(get_async_session)
) -> UserRepository:
    return UserRepository(session)


async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(
        user_repository=user_repository
    )


async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(
        user_repository=user_repository
    )
