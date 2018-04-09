# Documentación relacionada con la Base de Datos

## Docker postgres


Comandos de obtencion
sudo docker pull postgres

sudo docker run --name BD -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres

Una vez creado y cerrada la termianal si se quiere volver a ejecutar; usar:

sudo docker start BD


## Parametros de conexion a la BD [usuarios]

### Usuario adminsitrador
#### - Puede gestionar (crear, modificar y elimiar) tablas.
#### - Puede leer tablas
#### - Puede gestionar el contenido de las tablas
#### - Puede crear roles

usuario: postgres
contraseña: mysecretpassword

### Usuario solo lectura y escritura
#### - Puede interrogar tablas (SELECT)
#### - Puede gestionar el contenido de las tablas

usuario: read_write
contraseña: PasswordReadWrite

## Parametros de conexion a la BD [URL]

url: localhost:5432/postgres
