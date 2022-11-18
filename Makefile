SHELL:=/usr/bin/env bash


.PHONY: isort
isort:
	poetry run isort .

.PHONY: lint
lint:
	poetry run mypy playmobile tests
	poetry run flake8 playmobile tests
	poetry run lint-imports
	poetry run pytest --dead-fixtures

.PHONY: package
package:
	poetry run poetry check
	poetry run pip check
	poetry run safety check --full-report

.PHONY: test
test: lint package
	poetry run pytest
