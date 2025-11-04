SHELL := /bin/bash

VENV_NAME?=venv1
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3.12

# Default goal to be executed if no target is specified
.DEFAULT_GOAL := help

.PHONY: help setup clean 

# Color variables
CYAN    := \033[36m
RESET   := \033[0m

# Help: Displays available targets in the Makefile
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*? ## / {printf "$(CYAN)%-20s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Set up the Python virtual environment and install dependencies.
	@echo -e "$(CYAN)Creating Python virtual environment...$(RESET)"
	@python3.12 -m venv $(VENV_NAME)
	@echo -e "$(CYAN)Installing dependencies...$(RESET)"
	

clean: ## Remove the Python virtual environment and clean up installed packages
	@echo "Deleting the Python virtual environment..."
	@rm -rf $(VENV_NAME)
	@echo "Virtual environment and dependencies removed."
