run:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

lint:
	flake8

test:
	python manage.py test
