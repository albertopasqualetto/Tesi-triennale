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

.PHONY: help clean docs install lint test test-coverage format

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

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

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

install: ## install the package to the active Python's site-packages
	poetry install

test: ## run tests quickly with the default Python
	$(POETRY) pytest
	# cd docs && $(POETRY) make doctest

test-coverage: ## run tests with coverage
	$(POETRY) pytest --cov-config .coveragerc --cov-report term-missing --cov-report html --cov=mpai_cae_arp

format: ## format code
	$(POETRY) yapf --in-place --recursive ./mpai_cae_arp ./tests

lint: ## check style with pylint
	$(POETRY) pylint ./mpai_cae_arp ./tests

docs: ## generate Sphinx HTML documentation, including API docs
	$(DOCS) && $(POETRY) make html && $(OPEN) build/html/index.html
