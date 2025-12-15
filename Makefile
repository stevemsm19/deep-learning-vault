SHELL := /bin/bash

VENV_NAME?=venv
VENV_ACTIVATE=source $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3.12

# Default goal to be executed if no target is specified
.DEFAULT_GOAL := help

.PHONY: help setup clean

# Define color codes
CYAN := \033[36m
YELLOW := \033[33m
NC := \033[0m # No Color


# Help: Displays available targets in the Makefile
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*? ## / {printf "$(CYAN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Set up the Python virtual environment and install dependencies.
	@echo -e "$(CYAN)Creating Python virtual environment...$(NC)"
	@python3.12 -m venv $(VENV_NAME)
	@echo -e "$(CYAN)Installing dependencies...$(NC)"
	@$(VENV_ACTIVATE) && pip install --upgrade pip setuptools
	@$(VENV_ACTIVATE) && pip install -r requirements-dev.txt
	@$(VENV_ACTIVATE) && pip install -e .
	@echo -e "$(YELLOW)Activate with: source venv/bin/activate"

clean: ## Remove the Python virtual environment and clean up installed packages.
	@echo -e "$(CYAN)Deleting the Python virtual environment...$(NC)"
	@rm -rf $(VENV_NAME)
	@echo -e "$(CYAN)Virtual environment and dependencies removed.$(NC)"

typst-watch: ## Watch the csds-353-vault typst file and recompiles on changes
	@typst w documentation/csds-353-vault.typ

typst-compile: ## Compile the csds-353-vault typst file
	@typst c documentation/csds-353-vault.typ

backend: ## Run the FastAPI backend
	@uvicorn src.app.backend.main:app --port=8001

frontend: ## Run the Streamlit frontend
	@streamlit run ./src/app/frontend/Finai_Bot.py

docker: ## Run a local development environment with Docker Compose.
	@docker compose up -d --build

chroma: ## Run Chroma vector database with Docker
	@docker run -d --name chromadb-local -p 8000:8000 -v chroma_data:/chroma/chroma chromadb/chroma

check-ci: ## Check the pipeline process
	@echo -e "$(YELLOW)Checking black --check command....$(NC)"
	@black --check .
	@echo -e "$(CYYELLOWAN)Checking mypy command....$(NC)"
	@mypy .
	@echo -e "$(CYYELLOWAN)Checking plain compliance....$(NC)"
	@./ci/scripts/check-plain-compliance.sh
	@echo -e "$(CYYELLOWAN)Checking ipynb compliance....$(NC)"
	@./ci/scripts/check-ipynb-compliance.sh
	@echo -e "$(YELLOW)Checking for obsolete dependencies....$(NC)"
	@./ci/scripts/check-outdated.sh
