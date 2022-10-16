## Deployment

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) on the server & clone the project from GitHub.

2. Build the project:
```
make build
```

3. Deploy the project:
```
make up
```

4. Create SuperAdmin account:
```
docker-compose -f local.yml run django python manage.py createsuperuser
```
        
5. Creat new migrations based on the changes you have made to your models:
```
docker-compose -f local.yml run django python manage.py makemigrations
```
6. Synchronises the database state with the current set of models and migrations:
```
docker-compose -f local.yml run django python manage.py migrate
```
7. Collects the static files:
```
docker-compose -f local.yml run django python manage.py collectstatic
```
