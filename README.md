# Crossbox - App to handle reservations of [crossboxpalau.com](https://www.crossboxpalau.com)

Crossbox Palau is a Crossfit box located in Palau-solità i Plegamans, you can check all the links here https://linktr.ee/crossboxpalau.

It started managing the booking of sessions with a Doodle but soon the business started to demand something a bit more sophisticated and this tool was written totally tailored for this box.

The first versions only had the basics to have users and sessions. The latest ones include payment subscriptions based on [Stripe](https://stripe.com/) payment system. And it keeps evolving to fit the new needs of the box.

The production environment of this app is at https://reservations.crossboxpalau.com/.

You can register a new user but the owner of Crossbox Palau has to activate it because now the bottleneck for scaling up the business is the physical installations that doesn't allow more concurrent users.

You can find more detailed information about this project [in this page](https://oalfonso.com/projects/crossbox/).

The code is under the MIT license, so feel free to use it. There are no translations, as it is only for Spanish customers everything is in Spanish because is not planned to scale it to other countries so far. If you want to use it in other languages you have to implement the translations.

## Installation

As this app has payments that are processed with [Stripe](https://stripe.com/) we need an account before filling the environment variables.

### Docker

#### Requirements

- [`docker`](https://docs.docker.com/)
- [`docker-compose`](https://docs.docker.com/compose/)

Notice that now compose is a plugin of docker, but this project was made when compose had a different bin, so if you use compose as a plugin of docker, change "docker-compose" with "docker compose".

#### Env vars
```bash
cp .env.example .env
cp crossbox/static/js/custom/.env.js.example crossbox/static/js/custom/.env.js
```
And edit them. The minimum are:
```
DJANGO_STRIPE_PUBLIC_KEY (.env)
DJANGO_STRIPE_SECRET_KEY (.env)
stripe_publishable_key (.env.js)
```
Which can be obtained in your Stripe dashboard. Stripe offers a test environment, there's no need to use real payment data.

#### Run the webserver

```bash
docker-compose up
```

The database and the webserver will now be up.

#### Migrations

To create all the tables in the database Django uses something called migrations:

```bash
docker-compose exec django python manage.py migrate
```

#### Create admin user

```bash
docker-compose exec django python manage.py createsuperuser
```

#### Tests and linting

For testing we are using the Django testing module and for linting Flake8.

You can run both using `nox`.

```
docker-compose exec nox
```

### Without Docker

#### Requirements

- `Python>=3`
- `PostgreSQL`

#### Env vars
```bash
cp .env.example .env
cp crossbox/static/js/custom/.env.js.example crossbox/static/js/custom/.env.js
```
And edit them. The minimum are:
```
DB_HOST (.env)
DB_PORT (.env)
DB_NAME (.env)
DB_USER (.env)
DB_PASSWD (.env)
DJANGO_STRIPE_PUBLIC_KEY (.env)
DJANGO_STRIPE_SECRET_KEY (.env)
stripe_publishable_key (.env.js)
```
Stripe secrets can be obtained in your Stripe dashboard. Stripe offers a test environment, there's no need to use real payment data.

#### Install

Create a virtualenv with Python>=3 with your preferred tool and install the package and the dev requirements to run the tests:

```bash
pip install -e .
pip install -r requirements-dev.txt
```
In this snippet the installation of the module is set as editable in order to keep the code in the same location, but you can do as you wish.

#### Run the webserver

And run it
```bash
python manage.py runserver
```

#### Migrations

To create all the tables in the database Django uses something called migrations:

```bash
python manage.py migrate
```

#### Create admin user

```bash
python manage.py createsuperuser
```

#### Tests and linting

For testing we are using the Django testing module and for linting Flake8.

You can run both using `nox`.

```
nox
```
