.PHONY: \
	build \
	up \
	down \
	test \
	lint \
	format-check \
	check \
	push

.EXPORT_ALL_VARIABLES:

PROJECT_NAME := shelf

REGISTRY ?= ghcr.io
IMAGE_NAME ?= $(REGISTRY)/slavasuhoveev/shelf-api
TAG ?= develop

DOCKER_BUILD_OPTS ?=

build:
	docker compose build shelf_api

up: build
	docker compose up -d

down:
	docker compose down

test:
	docker compose build --no-cache shelf_tests
	docker compose run --rm shelf_tests

lint:
	poetry run poe lint

format-check:
	poetry run poe format-check

check: lint format-check

push:
	docker push $(IMAGE_NAME):$(TAG)
