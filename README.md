# Crossbox - App to handle reservations of [crossboxpalau.com](https://www.crossboxpalau.com)

Crossbox Palau is a Crossfit box located in Palau-solità i Plegamans, you can check all the links here https://linktr.ee/crossboxpalau.

It started managing the booking of sessions with a Doodle but soon the business started to demand something a bit more sophisticated and this tool was written totally tailored for this box.

The first versions only had the basics to have users and sessions. The latest ones include payment subscriptions based on Stripe payment system. And it keeps evolving to fit the new needs of the box.

The production environment of this app is at https://reservations.crossboxpalau.com/.

You can register a new user but the owner of Crossbox Palau has to activate it because now the bottleneck of the business is the physical installations and there's queue to access the service.

The code is under the MIT license, so feel free to use it. There are no translations, as it is only for Spanish customers everything is in Spanish because is not planned to scale it to other countries so far. If you want to use it in other countries you have to implement the translations.

## Installation
### Environment variables file
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

### Tests and linting

For testing we are using the Django testing module and for linting Flake8.

You can run both using `nox`.

```
nox
```
