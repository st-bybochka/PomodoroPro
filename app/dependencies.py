from fastapi import Depends, security, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.client import GoogleScient
from app.infrastructure.database import get_async_session
from app.exceptions import TaskNotFound, TokenNotCorrectException
from app.repository import TaskRepository, TaskCache, UserRepository
from app.infrastructure.cache import get_redis_connection
from app.service import TaskService, UserService, AuthService, HashService, JwtTokenService, hash_service
from app.config import settings
from app.service.auth_google_service import AuthGoogleService


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

async def get_google_client() -> GoogleScient:
    return GoogleScient()


async def get_task_service(
        task_repository: TaskRepository = Depends(get_task_repository),
        task_cache: TaskCache = Depends(get_cache_task_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )

async def get_hash_service() -> HashService:
    return HashService()

async def get_token_service() -> JwtTokenService:
    return JwtTokenService()


async def get_auth_login_service(
        user_repository: UserRepository = Depends(get_user_repository),
        token_service: JwtTokenService = Depends(get_token_service),
        hash_service: HashService = Depends(get_hash_service)

) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=settings,
        token_service=token_service,
        hash_service=hash_service
    )

async def get_auth_google_service(
        google_client: GoogleScient = Depends(get_google_client),
        token_service: JwtTokenService = Depends(get_token_service),
        hash_service: HashService = Depends(get_hash_service),
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_login_service)
) -> AuthGoogleService:
    return AuthGoogleService(
        user_repository=user_repository,
        token_service=token_service,
        hash_service=hash_service,
        google_client=google_client,
        auth_service=auth_service


    )


async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_login_service),
        token_service: JwtTokenService = Depends(get_token_service),
        hash_service: HashService = Depends(get_hash_service)
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service,
        token_service=token_service,
        hash_service=hash_service
    )

reusable_auth = security.HTTPBearer()

async def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_login_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_auth)
) -> int:

    try:

        user_id = await auth_service.get_user_id_from_access_token(token.credentials)
        return user_id

    except TokenNotCorrectException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )





