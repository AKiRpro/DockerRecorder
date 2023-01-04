SHELL := /bin/bash
CWD := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ME := $(shell whoami)

nothing:
	@echo "do nothing"


# CONTAINERS
containers:
	docker container ls

# NETWORK
network_create:
	docker network create -d bridge jibri_network

network_inspect:
	docker network inspect jibri_network


# DATABASE
db_up:
	docker container run \
		--name jibri_db \
		--rm \
		--detach \
		--env POSTGRES_USER=jibri_admin \
		--env POSTGRES_PASSWORD=jibri_secret \
		--env POSTGRES_DB=jibri \
		--publish 5432:5432 \
		--network=jibri_network \
		postgres

db_down:
	docker container stop jibri_db

db_logs:
	docker container logs --follow jibri_db

db_inspect:
	docker container inspect jibri_db

db_restore:
	pg_restore \
		--verbose \
		--no-owner \
		--host=127.0.0.1 \
		--port=5432 \
		--username=jibri_admin \
		--dbname=jibri \
		backup/jibri_2022_07_20_17_04_28.dump

# WORKER
worker_build:
	docker image build . --network jibri_network --tag jibri_worker

worker_up:
	docker container run \
		--name jibri_worker_${ROOM_ID} \
		--env ROOM_ID=${ROOM_ID} \
		--rm \
		--detach \
		--network jibri_network \
		--volume /home/akir/Projects/DockerLauncher/output/:/recording/output/ \
		jibri_worker

worker_down:
	docker container stop jibri_worker_${SESSION_ID}

worker_logs:
	docker container logs --follow jibri_worker_${SESSION_ID}

worker_inspect:
	docker container inspect jibri_worker_${SESSION_ID}
