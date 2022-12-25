FROM python:3.11-alpine3.16
LABEL maintainer="Alireza Raei"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .temp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ] ; \
      then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf tmp && \
    apk del .temp-build-deps && \
    adduser \
      --disabled-password \
      --no-create-home \
      django-user

# Update the environment variable inside the image
# All of our commands will be run from virtual environment
ENV PATH="/py/bin:$PATH"
#RUN mkdir -p /vol/web/static
#RUN mkdir -p /vol/web/media
#RUN adduser -D user
#RUN chown -R user:user /vol/
#RUN chmod -R 755 /vol/web

USER django-user
