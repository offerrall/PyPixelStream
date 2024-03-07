# Makefile

# handle per OS config
UNAME_S 						:= $(shell uname -s)
ROOT_DIR						:= $(PWD)
VENV_DIR						:= ./venv

# version of python
ENVIRONMENTS = all

help:
	@echo "Make targets:"
	@echo "  help         - this help"
	@echo "  all          - build all the things for running"
	@echo "  clean        - remove build and env"
	@echo 'USEFUL TARGETS'
	@echo "  freeze       - freeze current pip requirements into requirements.txt"

.DEFAULT_GOAL := all

# environment
SHELL := /bin/bash

# virtualenv
PYTHON_BIN      := $(shell which python3)
ACTIVATE_BIN 	  := venv/bin/activate
PIP_BIN 				:= venv/bin/pip
REPOS_DIR				:= repos

# target for running
all: venv 

clean:
	@$(RM) -r venv; \
	find . -name "*.pyc" -exec $(RM) -rf {} \;

venv: $(ACTIVATE_BIN) pip_requirements 

$(ACTIVATE_BIN):
	@test -d venv || virtualenv -p $(PYTHON_BIN) venv

# the language setting here is because we're testing in a container.
pip_requirements: $(ACTIVATE_BIN) $(VENV_DIR)/.pip_requirements

$(VENV_DIR)/.pip_requirements: requirements.txt
	@. venv/bin/activate; PYTHONWARNINGS='ignore:DEPRECATION' LANG=en_US.UTF-8 pip install --upgrade pip
	@. venv/bin/activate; PYTHONWARNINGS='ignore:DEPRECATION' LANG=en_US.UTF-8 pip install -r requirements.txt
	@touch $(VENV_DIR)/.pip_requirements

freeze:
	. venv/bin/activate && venv/bin/pip freeze > requirements.txt


