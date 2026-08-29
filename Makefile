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

PROJECT_NAME := shelf-api

REGISTRY ?= ghcr.io
IMAGE_NAME ?= $(REGISTRY)/slavasuhoveev/$(PROJECT_NAME)

# Default local tag
TAG ?= develop

DOCKER_BUILD_OPTS ?=

build:
	@docker compose build shelf_api

build-prod:
	@docker build \
		--target final \
		-t $(IMAGE_NAME):$(TAG) \
		.

up: build
	@docker compose up -d

down:
	@docker compose down

test:
	@docker compose build --no-cache shelf_tests
	@docker compose run --rm shelf_tests

lint:
	@poetry run poe lint

format-check:
	@poetry run poe format-check

check: lint format-check

push:
	@docker push $(IMAGE_NAME):$(TAG)
