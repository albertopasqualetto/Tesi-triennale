UNAME := $(shell uname)
POETRY := poetry run
DOCS := cd docs && $(POETRY) make clean

ifeq ($(UNAME), Linux)
	OPEN = xdg-open
endif
ifeq ($(UNAME), Darwin)
	OPEN = open
endif
ifeq ($(UNAME), Windows)
	OPEN = start
endif

.PHONY: help clean docs

clean: clean-build clean-pyc clean-ruff clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-ruff:
	rm -fr .ruff_cache/

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

install:
	poetry install

test:
	$(POETRY) pytest

format:
	$(POETRY) ruff check --fix ./src ./tests

lint:
	$(POETRY) ruff check ./src ./tests

docs:
	$(DOCS) && $(POETRY) make html && $(OPEN) build/html/index.html
