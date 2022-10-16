upbuild: build up

up:
	docker-compose -f local.yml up

build:
	docker-compose -f local.yml build

run:
	docker-compose -f local.yml run $(filter-out $@,$(MAKECMDGOALS))

restart:
	docker-compose -f local.yml restart $(filter-out $@,$(MAKECMDGOALS))


down:
	docker-compose -f local.yml down $(filter-out $@,$(MAKECMDGOALS))

destroy:
	docker-compose -f local.yml down -v

createsuperuser:
	docker-compose -f local.yml exec django /entrypoint ./manage.py createsuperuser

makemigrations:
	docker-compose -f local.yml run --rm django ./manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

migrate:
	docker-compose -f local.yml run --rm django ./manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

