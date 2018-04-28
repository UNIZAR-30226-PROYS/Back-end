FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN apk update && apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apk --purge del .build-deps

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]

COPY . /usr/src/app
