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
	python -m pytest -vx --cov=app --cov-report term-missing --cov-fail-under=95

data_test:
	echo wip

alembic_downgrade:
	docker-compose run app alembic downgrade base
