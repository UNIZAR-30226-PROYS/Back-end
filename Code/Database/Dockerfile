FROM postgres
WORKDIR /docker-entrypoint-initdb.d
ADD 00_code.sql /docker-entrypoint-initdb.d
ADD 01_funciones_de_consulta.sql /docker-entrypoint-initdb.d
ADD 02_poblado.sql /docker-entrypoint-initdb.d
EXPOSE 5432
