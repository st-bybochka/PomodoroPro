from fastapi import Depends, Request, security, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from exceptions import TokenExpired, TokenNotCorrect
from repository import TaskRepository, TaskCache, UserRepository
from cache import get_redis_connection
from service import TaskService, UserService, AuthService
from settings import settings


async def get_task_repository(
        session: AsyncSession = Depends(get_async_session)
) -> TaskRepository:
    return TaskRepository(session)


async def get_user_repository(
        session: AsyncSession = Depends(get_async_session)
) -> UserRepository:
    return UserRepository(session)


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


async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=settings
    )


async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )

reusable_auth = security.HTTPBearer()

async def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_auth)
) -> int:

    try:

        user_id = await auth_service.get_user_id_from_access_token(token.credentials)

    except TokenExpired as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    return user_id


