install:
	pip install poetry && \
	poetry install

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
	docker-compose run app alembic downgrade base

format:
	black .

generate_sdk:
	npm install
	python sdk_client_script.py
	npm run generate-client
