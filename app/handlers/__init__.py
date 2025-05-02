
from app.handlers.tasks_handlers import router as tasks_router
from app.handlers.user_handlers import router as user_router
from app.handlers.auth_login_handlers import router as auth_login_router
from app.handlers.auth_google_handler import router as auth_google_router

routers = [tasks_router, user_router, auth_login_router, auth_google_router]