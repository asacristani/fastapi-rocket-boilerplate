# TODO: add testing coverage
# TODO: add more? check other repositories 

# 🐍💨 FastAPI Core
FastAPI core to build an API based in Python with its most modern technologies!

## 🧩 Features
# TODO: improve stetic
- Use -> Makefile
- DEV encapsulation -> Docker compose
- Dependencies -> Poetry
- DB -> PostgreSQL
- Migrations -> Alembic
- Authentication -> Oauth2
  - access and refresh tokens
  - email verification (later)
  - role scopes (later)
- ORM -> SQLModel
  - Base model with all the DB logic needed
  - Changes/events record
- Admin dashboard -> sqladmin
  - Config user
  - Delete as soft delete
  - AuthX for accessing
  - Event records
- Testing -> Pytest and Unittest
  - Unit testing mocking the rest of services
  - Integrity testing
- Pre commit -> flake, XXXX
- CI -> Github actions

All this using Python 3.11

## ⚙️ Requirements
# TODO: add links
- Python 3.11
- Docker
- GNU system?


## 🎛️  Use
### 🔧 Installation
Install the requirements with Poetry for developing, testing and debugging purposes.

`make install`

If you want to use the pre-commit with the same style checks than the CI pipeline:

`pre-commit install`

You can test the pre-commit without comiting running `pre-commit run --all-files`
### 🔌 Build and run
Build and run the Docker services for using in Local.

`make run`

Congrats! the API is working at this point, you can check:
- Docs: http://localhost:8000/docs
- Admin: http://localhost:8000/admin

For admin, use:
```shell
ADMIN_USER=superuser
ADMIN_PASS=admin
```

### 🧪 Test
Run pytest with coverage for unit testing.

`make test`

You do not need to run inside Docker container.

The DB is replaced by a SQLite db in memory 😎

### 🚚 Migrations
Use Alembic for DB migrations.

If you create a new model, import it in: `app/core/db/migrations/models.py`

After this, or modified a previous model, create the migration document:
```
docker-compose run app alembic revision --autogenerate -m "your commit"
```
If you are trying to do something complicated, maybe you need to fix the file manually.


Migration file should be created inside the Docker container because the DB url is referencing the Docker network domain.


Migrations will run when docker compose up, but you can run them manually:
```
docker-compose run app alembic upgread head
```


## 🛠 Extend
Basically, you will want to create new services that contain endpoints and models.
And of course, it is almost completely sure you need to add new extra dependencies.

You can use the service `user` as reference.

### 📦 Models
If you want to create a new model to be stored in the DB, you should follow these steps:
1. Create a new Class based in ModelCore with `table=True`
```python
from app.core.base.models import ModelCore

class NewModel(ModelCore, table=True):
    unique_property: str
```
2. Import the new class into the migration model file `app.core.db.migrations.models`
3. Create a new migration
4. Create an AdminModel in `app.services.admin.models`:
```python
from app.core.admin.models import ModelViewCore

class NewModelAdmin(ModelViewCore, model=NewModel):
    # You can add config settings here for the Admin panel.
    pass
```
5. Append it in `admin_models` into `app.services.admin.config`

### 🚏 Routes
If you want to create a new view protected by auth, you should include the `get_current_user` dependency.

Here you have an example of a new service with a protected route:
```python
from fastapi import APIRouter, Depends

from app.core.auth.functions import get_current_user

router = APIRouter(
    prefix="/security",
    tags=["security"]
)

@router.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    """ Endpoint for auth test"""
    return {"message": f"¡Hola, {current_user}! This is a protected url and you are inside!"}
```
And then append the router in `routers` into `app.main`

For creating new users, they can register by themselves or be added by Admin panel.

### 🏗️ Dependencies
Use Poetry like:
```
poetry add <new_dependency>
```

### 🗜️ Enviroment variables
You should change the next env vars in `.env`:
- Password hash:
  - SECRET_KEY: run `TODO` to generate a new one
- Admin superuser:
  - ADMIN_USER
  - ADMIN_PASS

Also, it is possible you want to modify the expiry time of access/refresh tokens.

## 🚀 Future features
### Admin
- Search events by model AND id
- Fix popup for reverse_delete
- Relationship of records into model details (performance)

### Others
- Add mypy and pylint to the Pre-commit
- Integrity tests
- Use async/await for routes and database connections
- Aync/cron tasks with Celery + RabbitMQ
- Authentication client with Google
- TypeScript client
- Deployment with Kubernetes in Google Cloud by Terraform