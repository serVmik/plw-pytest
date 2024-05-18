install:
	poetry install;
	playwright install;
	playwright install --with-deps

lint:
	poetry run flake8

test:
	pytest

check: lint test


