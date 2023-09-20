from fastapi import FastAPI, HTTPException
from sqladmin import Admin
from sqlalchemy.exc import OperationalError

from .settings import settings
from .core.db.engine import get_engine
from .services.user.routes import router as user_router
from .services.admin.config import admin_models, admin_views
from .core.admin.auth import AdminAuth
from .core.middleware.nocache import NoCacheMiddleware
from .core.middleware.db_session_context import DBSessionMiddleware


app = FastAPI()

# ROUTERS
routers = [user_router]
for router in routers:
    app.include_router(router)

# ADMIN
admin = Admin(app, get_engine(), templates_dir="app/services/admin/templates",
              authentication_backend=AdminAuth(secret_key=settings.secret_key))
for item in admin_models + admin_views:
    admin.add_view(item)

# MIDDLEWARES
app.add_middleware(NoCacheMiddleware)
app.add_middleware(DBSessionMiddleware, custom_engine=get_engine())


@app.get("/")
def read_root():
    return {"msg": "Welcome to the backend core in in FastAPI!"}


def check_db_connection():
    try:
        with get_engine().connect():
            return True
    except OperationalError:
        return False


@app.get("/check_health")
async def check_health():
    """
    Check all the services in the infrastructure are working
    """
    db_status = check_db_connection()
    if db_status:
        return {"status": "healthy", "message": "Database connection is good"}
    else:
        raise HTTPException(status_code=503, detail="Service unavailable")
