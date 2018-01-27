FROM python:3.5.4

# explicitly set user/group IDs
RUN groupadd -r uwsgi --gid=999 && useradd -r -g uwsgi --uid=999 uwsgi

# Configue timezone
ENV TIMEZONE "America/Mexico_City"

RUN echo "$TIMEZONE" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

# Folder structure
RUN mkdir -p /app \
    && chown -R uwsgi:uwsgi /app

WORKDIR /app

EXPOSE 8000

# Install uWSGI and pipenv
RUN set -ex; \
    pip install pipenv uWSGI --no-cache-dir;

COPY . /app

# Install dependencies
RUN set -xe \
    && pipenv install --deploy --system

CMD [ "uwsgi", "/app/uwsgi.ini" ]
