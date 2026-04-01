.PHONY: run test lint format

run:
	python -m neonctl.main

test:
	pytest -q

lint:
	ruff check .

format:
	black .
