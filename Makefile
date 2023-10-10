# Define variables for Python and pip executables
PYTHON ?= python3
PIP ?= pip3

install:
	$(PIP) install poetry && \
	poetry install

run:
	docker-compose build && \
	docker-compose up

build:
	docker-compose build

up:
	docker-compose up

test:
	poetry run pytest -vx --cov=app --cov-report term-missing --cov-fail-under=95

data_test:
	@echo wip

alembic_downgrade:
	docker-compose run app alembic downgrade base

format:
	black .

generate_sdk:
	$(PYTHON) sdk_client_script.py
	npm run generate-client
