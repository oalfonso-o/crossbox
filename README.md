# Crossbox - App to handle reservations of [crossboxpalau.com](https://www.crossboxpalau.com)

Crossbox Palau is a Crossfit box located in Palau-solità i Plegamans managed by Roger López.

It started managing the booking of sessions with a [Doodle](https://doodle.com/en/) but soon the business started to demand something a bit more sophisticated and this tool was written totally tailored for this box.

The first versions only had the basics to have users and sessions. The latest ones include payment subscriptions based on Stripe payment system. And it keeps evolving to fit the new needs of the box.

## Installation
### 1. Environment variables file
```bash
cp .env.example .env
cp crossbox/static/js/custom/.env.js.example crossbox/static/js/custom/.env.js
```
And edit wherever you need

### 2 Run the app
- With DOCKER (it works with postgres)
```bash
docker-compose up
```
- Or locally, for what you need:
  - a local db
  - a virtualenv with python>=3
  - install the project module in your environment as editable and also it's requirements
```bash
pip install -e .
pip install -r requirements-dev.txt
```
And run it
```bash
python manage.py runserver
```

## SetUp Database (with containers runnings)
### Migrations
- Docker
```bash
docker-compose exec django python manage.py migrate
```
- Local
```bash
python manage.py migrate
```
### Superuser
- Docker
```bash
docker-compose exec django python manage.py createsuperuser
```
- Local
```bash
python manage.py createsuperuser
```

### Packaging
- Bump version in file setup.py (version='X.Y')
- Create the wheel:
```bash
pip wheel . --no-deps
```
- Bring the wheel wherever you need it as a pypi repo for example


### Tests and linting
- Docker:
```bash
docker-compose exec django nox
```
- Local
```bash
nox
```
