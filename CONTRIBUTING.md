# CONTRIBUTING

## How to build a DOCKER image

```
docker build -t falsk-smorest-api .
```
##  How to run docker app in docker container

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" falsk-smorest-api
```
##  How to run docker app locally

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest-api-flask sh -c "flask run"

```

## How to run migrations

```
falsk db upgrade
```