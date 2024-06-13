# CONTRIBUTING

## How to build a DOCKER image

```
prototype
docker build -t <name of the image> .

example:
docker build -t rest_api_flask_python .
```

## How to run the app in Docker container
```
docker run -d -p 5000:5000 rest_api_flask_python

here -d stands for demon mode and -p for port forwarding, we can also use

docker run -dp 5000:5000 rest_api_flask_python
```

##  How to run the app in docker container in debug mode

```
When we replace image's /app directory with host's source code folder, this causes the source code to change in the Docker container while it's running. And, since we've ran Flask with debug mode on, the Flask app will automatically restart when the code changes. The command for this will be

docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest_api_flask_python
```

## To run the app and database locally with Docker Compose
```
docker compose up --build --force-recreate --no-deps web
```

##  How to run docker app locally

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest_api_flask_python sh -c "flask run --host 0.0.0.0"

```

## How to run migrations

```
flask db init
flask db migrate
falsk db upgrade
```

## How to run rq worker

```
docker run -w /app rest_api_flask_python sh -c "rq worker -u <redis_url> <name_od_queue>"
```