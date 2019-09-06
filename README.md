# Crossbox - App to handle reservations of Crossbox Palau

## Installation
### 1. Environment variables file
```bash
cp .env.example .env
```
And edit wherever you need

### 2 Run the app
- With DOCKER (it works with postgres)
```bash
docker-compose up
```
- Or locally, for what you need:
  - a local dbs
  - a virtualenv with python>=3
  - install the project module in your environment as editable and also it's requirements
```bash
pip install -e .
pip install -r requirements-dev.txt
```

## SetUp DataBase
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
