#!/usr/bin/env bash
# Idempotent bootstrap for the Cloud Agent development environment.
# Installs Node dev dependencies (eslint) and prepares a Python virtualenv
# for the Streamlit turnover-analysis app.
set -euo pipefail

cd "$(dirname "$0")/.."

# python3-venv is required to create virtual environments but is not always
# present on the base image.
if ! dpkg -s python3-venv >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo apt-get install -y --no-install-recommends python3-venv
fi

# Node dev dependencies (eslint) for the static site.
npm install

# Python virtualenv for the Streamlit turnover-analysis app.
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r turnover-analysis/requirements.txt

echo "Environment setup complete."
