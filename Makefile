# Makefile for Investment Strategies Simulator

.PHONY: install shell run-daily run-rolling test format lint pre-commit

install:
	poetry install

shell:
	poetry shell

run-daily:
	poetry run python src/investment_strategies/main_daily.py

run-rolling:
	poetry run python src/investment_strategies/main_rolling_weekly.py

test:
	poetry run pytest

format:
	poetry run black src/ tests/

lint:
	poetry run ruff check src/ tests/ --fix

pre-commit:
	poetry run pre-commit run --all-files
