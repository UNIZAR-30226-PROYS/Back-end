FROM postgres
WORKDIR /docker-entrypoint-initdb.d
ADD code.sql /docker-entrypoint-initdb.d
ADD funciones_de_consulta.sql /docker-entrypoint-initdb.d
EXPOSE 5432
