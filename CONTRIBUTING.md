# CONTRIBUTING

## How to build a DOCKER image

```
prototype
docker build -t <name of the image> .

example:
docker build -t falsk-smorest-api .
```

## How to run the app in Docker container
```
docker run -d -p 5000:5000 falsk-smorest-api

here -d stands for demon mode and -p for port forwarding, we can also use

docker run -dp 5000:5000 falsk-smorest-api
```

##  How to run the app in docker container in debug mode

```
When we replace image's /app directory with host's source code folder, this causes the source code to change in the Docker container while it's running. And, since we've ran Flask with debug mode on, the Flask app will automatically restart when the code changes. The command for this will be

docker run -dp 5000:5000 -w /app -v "$(pwd):/app" falsk-smorest-api
```
##  How to run docker app locally

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest-api-flask sh -c "flask run --host 0.0.0.0"

```

## How to run migrations

```
falsk db upgrade
```