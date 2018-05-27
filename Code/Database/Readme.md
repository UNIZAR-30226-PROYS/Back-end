# Documentación relacionada con la Base de Datos

## Docker postgres


Desde este directorio:

docker build -t cierzo_database .

docker run --name cierzoDB -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 cierzo_database

Una vez creado y cerrada la termianal si se quiere volver a ejecutar; usar:

sudo docker start cierzoBD


## Parametros de conexion a la BD [usuarios]

### Usuario adminsitrador
#### - Puede gestionar (CREATE, ALTER, DROP) tablas.
#### - Puede interrogar tablas (SELECT)
#### - Puede gestionar el contenido (UPDATE, DELETE, INSERT) de las tablas
#### - Puede crear roles

usuario: postgres
contraseña: mysecretpassword

### Usuario solo lectura y escritura
#### - Puede interrogar tablas (SELECT)
#### - Puede gestionar el contenido (UPDATE, DELETE, INSERT) de las tablas

usuario: read_write
contraseña: PasswordReadWrite

## Parametros de conexion a la BD [URL]

url: localhost:5432/postgres
