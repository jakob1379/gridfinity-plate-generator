.PHONY: install install-all update-deps upgrade run build clean deploy bump test run

# You can set ?= variables from the command line.
SHELL = /bin/bash
COMPOSE_PROJECT_NAME ?= gridfinity-plate-generator

install-all: install build

install:
	poetry install
	poetry run pre-commit install

update-deps:
	poetry update
	poetry run pre-commit update

upgrade: update-deps install

docker:
	docker build --no-cache -t $COMPOSE_PROJECT_NAME .

clean:
	docker compose down

deploy:
	docker compose up -d --remove-orphans

update-changelog:
	poetry run cz bump --yes --changelog

test:
	poetry run bash -c "coverage run -m pytest -v && coverage xml"

run:
	poetry run streamlit run app.py
