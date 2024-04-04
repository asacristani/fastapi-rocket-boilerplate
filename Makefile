install:
	# Requirements 
	pip install poetry && \
	poetry install
	# pre-commit
	npm install -D @trunkio/launcher

run:
	docker-compose build && \
	docker-compose up

build:
	docker-compose build

up:
	docker-compose up

test:
	pytest -vx --cov=app --cov-report term-missing --cov-fail-under=95

data_test:
	echo wip

alembic_downgrade:
	docker-compose run app alembic -c /app/app/core/db/migrations/alembic.ini downgrade base

migration_file:
	docker-compose run app alembic -c /app/app/core/db/migrations/alembic.ini revision --autogenerate -m "your commit"

format:
	black .

generate_sdk:
# Need the docker running 
	npm install --prefix ./generate_client
	python generate_client/sdk_client_script.py
	npm run generate-client --prefix ./generate_client
