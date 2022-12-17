FROM python:3.11-alpine3.16
LABEL maintainer="Alireza Raei"

ENV PYTHONUNBUFFERED 1

#RUN apk add --update --no-cache postgresql-client jpeg-dev
#RUN apk add --update --no-cache --virtual .temp-build-deps \
#    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
#RUN apk del .temp-build-deps

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf tmp && \
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
