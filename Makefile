run:
	python manage.py runserver 0.0.0.0:8000

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

init:
	python manage.py loaddata crossbox/fixtures/users
	python manage.py loaddata crossbox/fixtures/subscribers
	python manage.py loaddata crossbox/fixtures/hours
	python manage.py loaddata crossbox/fixtures/days
	python manage.py loaddata crossbox/fixtures/tracks
	python manage.py loaddata crossbox/fixtures/capacity_limits
	python manage.py loaddata crossbox/fixtures/week_templates
	python manage.py loaddata crossbox/fixtures/session_templates
	python manage.py loaddata crossbox/fixtures/session_types

resetdb:
	python manage.py reset_db --noinput
	make migrate
	make init

lint:
	flake8

test:
	python manage.py test
