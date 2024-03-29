FROM python:3.12
#EXPOSE 5000 not required for gunicorn
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
#CMD [ "flask","run","--host","0.0.0.0"]
CMD ["/bin/bash","docker-entrypoint.sh"]