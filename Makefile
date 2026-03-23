ENV ?= stage
TECH ?= python
SUITE ?= smoke
REPO ?= api-tests
MODE ?= local
PORT ?= 8000

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt -r requirements-dev.txt

run:
	uvicorn orchestrator.main:app --reload --app-dir src --port $(PORT)

test:
	pytest

lint:
	ruff check src tests

format:
	ruff format src tests

typecheck:
	mypy src

run-python-tests:
	cd ../$(REPO) && TARGET_ENV=$(ENV) ENV_FILE=.env.$(ENV) pytest -m $(SUITE)

run-java-tests:
	cd ../$(REPO) && mvn test -Dsuite=$(SUITE) -Denv=$(ENV) -DenvFile=.env.$(ENV)

run-ts-tests:
	cd ../$(REPO) && TARGET_ENV=$(ENV) ENV_FILE=.env.$(ENV) npm test -- --suite=$(SUITE) --env=$(ENV)

demo-plan:
	curl -X POST http://127.0.0.1:$(PORT)/plan \
	  -H "Content-Type: application/json" \
	  -d @examples/sample_multi_repo_request.json

demo-execute:
	curl -X POST http://127.0.0.1:$(PORT)/execute \
	  -H "Content-Type: application/json" \
	  -d @examples/sample_multi_repo_request.json
