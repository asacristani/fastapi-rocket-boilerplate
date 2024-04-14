install:
	# Requirements 
	pip install poetry && \
	poetry install
	# pre-commit
	curl https://get.trunk.io -fsSL | bash

run:
	docker-compose build && \
	docker-compose up

build:
	docker-compose build

up:
	docker-compose up

test:
	pytest -vx --cov=app --cov-report term-missing --cov-fail-under=95

test_no_migrations:
	pytest -m 'not alembic' -vx --cov=app --cov-report term-missing --cov-fail-under=95

test_only_migrations:
	pytest -m 'alembic'

data_test:
	echo wip

alembic_downgrade:
	docker-compose run app alembic -c /app/app/core/db/migrations/alembic.ini downgrade base

migration_file:
	docker-compose run app alembic -c /app/app/core/db/migrations/alembic.ini revision --autogenerate

format:
	trunk fmt

generate_sdk:
# Need the docker running 
	npm install --prefix ./generate_client
	python generate_client/sdk_client_script.py
	npm run generate-client --prefix ./generate_client
