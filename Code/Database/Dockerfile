FROM postgres

RUN mkdir -p /usr/src/datosPoblar
WORKDIR /usr/src/datosPoblar
COPY artistas /usr/src/datosPoblar/artistas
COPY canciones /usr/src/datosPoblar/canciones
COPY caratulas /usr/src/datosPoblar/caratulas

WORKDIR /docker-entrypoint-initdb.d
ADD 00_code.sql /docker-entrypoint-initdb.d
ADD 01_funciones_de_consulta.sql /docker-entrypoint-initdb.d
ADD 02_poblado.sql /docker-entrypoint-initdb.d
EXPOSE 5432
