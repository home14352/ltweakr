.PHONY: run test lint format dev-setup

dev-setup:
	python -m pip install -e .[dev]
.PHONY: run test lint format

run:
	python -m neonctl.main

test:
	python -c "import pytest" >/dev/null 2>&1 || $(MAKE) dev-setup
	python -m pytest -q

lint:
	python -c "import ruff" >/dev/null 2>&1 || $(MAKE) dev-setup
	python -m ruff check .

format:
	python -c "import black" >/dev/null 2>&1 || $(MAKE) dev-setup
	python -m black .
	pytest -q
