FROM python:3.8.5-alpine

# Set working directory to src inside container 
WORKDIR /src

# Install basic development utilities
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del mariadb-dev
RUN apk add netcat-openbsd
RUN apk add bash

# Copy the src folder
COPY ./src /src
# Copy the local dev requirements into src
COPY ./src/requirements.txt /src/requirements.txt
# Copy .env into src
COPY ./.env /src/.env
# Copy docker entrypoint
COPY ./docker/entrypoint.sh /

# Install all prod + local packages
RUN pip install -r requirements.txt

RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]