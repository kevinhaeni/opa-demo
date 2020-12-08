# pre-requisites:
# sudo apt install python3
# sudo apt install python3-pip
# sudo apt install make

.PHONY: build
build: install-dev

.PHONY: install-dev
install-dev:
	pip3 install python3-flask
	pip3 install Flask-OPA

.PHONY: demo
demo:
	export FLASK_ENV=development
	export FLASK_APP=app.py
	flask run

.PHONY: start-opa
start-opa:
	nohup opa run -s -w examples &

.PHONY: stop-opa, kill
stop-opa:
	kill $(ps | grep opa | awk '{print $1}')

.PHONY: help
help: 
	@echo "make start-opa"
	@echo "       starts the opa server"
	@echo "make stop-opa"
	@echo "       stops the opa server" 
	@echo "make demo"
	@echo "       runs the demo project"
	@echo "make test"
	@echo "       run tests"
	@echo "make coverage"
	@echo "       runs the tests and coverage"
	@echo "make lint"
	@echo "      run lints of interest for the code"
	@echo "make install"
	@echo "      install all requirements"
	@echo "make install-dev"
	@echo "      install all requirements for development"
	@echo "make build"
	@echo "      runs lints, tests and coverage"
