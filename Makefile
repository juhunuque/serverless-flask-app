app-container = app
db-container = db
migrate-container = migration
docker-command = docker-compose -f docker-compose.yml

init:
	$(MAKE) build
	$(MAKE) up

build:
	docker-compose -f docker-compose.yml rm -vsf
	docker-compose -f docker-compose.yml down -v --remove-orphans
	docker-compose -f docker-compose.yml build

up:
	docker-compose -f docker-compose.yml up -d ${db-container}
	$(MAKE) migrate
	docker-compose -f docker-compose.yml up -d ${app-container}

migrate:
	docker-compose -f docker-compose.yml up -d ${migrate-container}

stop:
	docker-compose -f docker-compose.yml rm -vsf
	docker-compose -f docker-compose.yml down -v --remove-orphans

down:
	docker-compose down

