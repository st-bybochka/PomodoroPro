from handlers.ping import router as ping_router
from handlers.tasks import router as tasks_router
from handlers.category import router as category_router

routers = [category_router, tasks_router, ping_router]