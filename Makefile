SHELL := /bin/bash

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3.12

# Default goal to be executed if no target is specified
.DEFAULT_GOAL := help

.PHONY: help setup clean 

# Define color codes
CYAN    := \033[36m
NC='\033[0m' # No Color

# Help: Displays available targets in the Makefile
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*? ## / {printf "$(CYAN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Set up the Python virtual environment and install dependencies.
	@echo -e "$(CYAN)Creating Python virtual environment...$(NC)"
	@python3.12 -m venv $(VENV_NAME)
	@echo -e "$(CYAN)Installing dependencies...$(NC)"
	

clean: ## Remove the Python virtual environment and clean up installed packages
	@echo -e "$(CYAN)Deleting the Python virtual environment...$(NC)"
	@rm -rf $(VENV_NAME)
	@echo -e "$(CYAN)Virtual environment and dependencies removed.$(NC)"
