
# Botnet

Utility for load testing telegram bots via using fake accounts. Integrated web admin panel for process management.


## Installation

#### 1. Install [Docker](https://www.docker.com)
#### 2. Create .env file at the root of the project

```bash
  DEBUG = 1 or 0
  SECRET_KEY = django random secret key
  DJANGO_ALLOWED_HOSTS = localhost 127.0.0.1 etc

  POSTGRES_HOST = postgres
  POSTGRES_PORT = 5432
  POSTGRES_DB = your db name
  POSTGRES_USER = your db user
  POSTGRES_PASSWORD = your db password

  REDIS_HOST = redis
  REDIS_PORT = 6379

  APP_ID = your telegram app id
  APP_HASH = your telegram app hash
```
For create **django random secret key** you can use
```bash
  pip3 install django
  python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Also you can get telegram **app id** and **app hash** in https://my.telegram.org/auth?to=apps
## Run project

Start server
```bash
  docker-compose up
```

Create superuser
```bash
  docker-compose exec web python manage.py createsuperuser
```

After go to http://127.0.0.1/admin