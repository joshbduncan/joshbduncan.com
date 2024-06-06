VENV:=venv
BIN:=$(VENV)/bin
PWD := $(realpath $(dir $(abspath $(firstword $(MAKEFILE_LIST)))))

.DEFAULT_GOAL := help
.PHONY: help
##@ General
help: ## Display this help section
	@echo $(MAKEFILE_LIST)
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development
venv: requirements-dev.txt ## build a virtual environment for development
	python -m venv $(VENV)
	$(BIN)/pip install -r requirements-dev.txt

imgspecs: imgspecs.sh ## get all static image file dimensions
	find app/static/images -type f -name "[^.]*" | sort | ./imgspecs.sh

server: ## startup the dev server
	$(BIN)/flask run

shell: ## startup the flask shell
	$(BIN)/flask shell

test-freeze: # freeze the blog and start up dev server on static files
	$(BIN)/python blog.py --run

##@ Build
build: ## freeze the blog for deployment
	$(BIN)/python blog.py --build

render: ## freeze the blog for deployment on render
	pip install -r requirements-github.txt
	python blog.py --build
