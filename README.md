<p align="center">
  <img src="https://lh3.googleusercontent.com/d/1ybx89iD_4jebLFgYqNAK4HxQOrniWj3y=s220?authuser=0">
</p>
<p align="center">
  <a href="https://github.com/AdrianPayne/fastapi-core/actions/workflows/ci.yml" target="_blank">
      <img src="https://github.com/AdrianPayne/fastapi-core/actions/workflows/ci.yml/badge.svg" alt="Test">
  </a>
  <a href="https://www.python.org/downloads/release/python-3110/" target="_blank">
      <img src="https://img.shields.io/badge/Coverage-96.26%25-%2347C21F?logo=github" alt="Coverage">
  </a>
  <a href="https://www.python.org/downloads/release/python-3110/" target="_blank">
      <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python 3.11">
  </a>
</p>
<p align="center">
  <i>🐍💨 FastAPI Rocket Boilerplate to build an API based in Python with its most modern technologies!</i>
</p>

---

<p align="center">
  <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"
      alt="Python">
  </a>
  <a href="https://fastapi.tiangolo.com/">
      <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="Fastapi">
  </a>
  <a href="https://www.postgresql.org/">
      <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"
      alt="Postgresql">
  </a>
  <a href="https://docs.celeryq.dev/en/stable/">
      <img src="https://img.shields.io/badge/celery-%2337814A.svg?&style=for-the-badge&logo=celery&logoColor=white" alt="Celery"/>
  </a>
  
  <a href="https://www.rabbitmq.com/">
      <img src="https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white" alt="Rabbitmq">
  </a>
  <a href="https://redis.com/" target="_blank">
      <img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  </a>
  <a href="https://www.docker.com/">
      <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  </a>
  <a href="https://www.docker.com/">
      <img src="https://img.shields.io/badge/Pulumi-8A3391?style=for-the-badge&logo=pulumi&logoColor=white" alt="Pulumi">
  </a>
</p>

<p align="center"> Also sqlmodel, pydantic, alembic, poetry, ...</p>

---

## 🧩 Features

- **Infrastructure**: the common services that every backend needs, served in local by Docker Compose
and in Google Cloud by Pulumi.
- **Easy**: all the commands ready by Makefile.
- **Fast**: thanks to Fastapi and async programming.
- **Async**: Celery using RabbitMQ as broker and Redis as backend.
- **ORM**: custom sqlmodel orm as django orm and mongoengine.
- **Authentication**: OAuth2 with access/refresh tokens.
- **Admin dashboard**: custom admin dashboard as django by sqladmin.
- **Reliable**: CI, integrity testing and covered by unit test at 95%.
- **Frontend friendly**: auto generation of SDK Typescript client.


## ⚙️ Requirements
- [Python 3.11](https://www.python.org/downloads/release/python-3114/)
- [Docker](https://docs.docker.com/engine/install/)
- [Node](https://nodejs.org/en) only for SDK frontend generation
- [Pulumi](https://www.pulumi.com/) only for deploying

## 🎛️  Use
### 🔧 Installation
1. Clone the repo


2. Install the requirements with Poetry for developing, testing and debugging purposes.

`make PYTHON=python PIP=pip install`

3. If you want to use the pre-commit with the same style-check that the CI pipeline:

`pre-commit install`

>ℹ️ You can test the pre-commit without comiting running `pre-commit run --all-files`

### 🔌 Build and run
Build and run the Docker services for using in Local.

`make run`

Congrats! the API is working at this point, you can check:
- Docs: http://localhost:8000/docs
- Admin: http://localhost:8000/admin
- RabbitMQ: http://localhost:15672/

For admin, use:
```shell
ADMIN_USER=superuser
ADMIN_PASS=admin
```

For generating the SDK frontend client (the app should be running):
```shell
make generate_sdk
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

### 🗜️ Environment variables
You should change the next env vars in `.env`:
- Password hash:
  - SECRET_KEY: run in the terminal `openssl rand -base64 32` to generate a new one
- Admin superuser:
  - ADMIN_USER
  - ADMIN_PASS

Also, it is possible you want to modify the expiry time of access/refresh tokens.

## 🚀 Deploy
We use Pulumi for deploying.


### Google Cloud
The DB will be deployed in GCP SQL service.

The rest of the services will be deployed in GCP GKE.

1. Log in Google cloud
```shell
gcloud auth application-default login
```
2. Create a new project in Google console
3. Set the project in gcloud
```shell
gcloud config set project <YOUR_GCP_PROJECT_ID>
```
To find it, you can run:
```shell
gcloud projects list 
```
4. Modify `Pulumi-dev.yaml` with your GCP project and region.
5. Modify the begging of `__main__.py` with your variables
6. run:
```
pulumi up
```

✅ It is done, your project is alive!


## 🔮 Future features

### Deployment
- [x] Deployment with Kubernetes in Google Cloud by Pulumi
- [ ] Deployment with Kubernetes in AWS by Pulumi

### Monitoring
- [ ] Add logging
- [ ] Add Sentry
- [ ] Add Flower

### Testing
- [ ] Integrity tests
- [ ] Cover 100% with unit-testing
- [ ] Add mypy and pylint to the Pre-commit

### Async
- [ ] Use 100% async/await for routes and database connections

### Auth
- [ ] Authentication client with Google

### Admin
- [ ] Search events by model AND id
- [ ] Fix popup for reverse_delete
- [ ] Relationship of records into model details (performance)
