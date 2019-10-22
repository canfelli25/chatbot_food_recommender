FROM python:3.6-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev  && apk add dos2unix --update-cache
RUN pip3 install psycopg2
ENV APP_SETTINGS config.Config
ENV DATABASE_URL ${DATABASE_URL}

COPY . /api
WORKDIR /api

# install requirements
RUN pip3 install -r requirements.txt

# expose the app port
EXPOSE 5001

RUN pip3 install gunicorn
RUN dos2unix /api/entrypoint.sh

# run the app server
CMD ["/bin/sh", "/api/entrypoint.sh"]