#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e . --break-system-packages
python -m neonctl.main
