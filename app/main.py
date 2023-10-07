import pika
import redis
from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.exc import OperationalError

from .core.admin.auth import AdminAuth
from .core.celery import celery
from .core.db.engine import get_engine
from .core.middleware.db_session_context import DBSessionMiddleware
from .core.middleware.nocache import NoCacheMiddleware
from .services.admin.config import admin_models, admin_views
from .services.user.routes import router as user_router
from .settings import settings

app = FastAPI()

# ROUTERS
routers = [user_router]
for router in routers:
    app.include_router(router)

# ADMIN
admin = Admin(
    app,
    get_engine(),
    templates_dir="app/services/admin/templates",
    authentication_backend=AdminAuth(secret_key=settings.secret_key),
)
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
    ok_code = "running"
    ko_code = "down"

    # DB check
    db_status = check_db_connection()
    if db_status:
        db_status = ok_code
    else:
        db_status = ko_code

    # Celery check
    celery_status = celery.control.inspect().ping()
    if celery_status:
        celery_status = ok_code
    else:
        celery_status = ko_code

    # RabbitMQ check
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.rabbit_host)
        )
        connection.close()
        rabbitmq_check = ok_code
    except Exception:
        rabbitmq_check = ko_code

    # Redis check
    try:
        redis_client = redis.StrictRedis(
            host=settings.redis_host, port=settings.redis_port
        )
        redis_client.ping()
        redis_status = ok_code
    except Exception:
        redis_status = ko_code

    return {
        "db": db_status,
        "celery": celery_status,
        "rabbitmq": rabbitmq_check,
        "redis": redis_status,
    }
