
## Docker postgres


Comandos de obtencion
sudo docker pull postgres

sudo docker run --name BD -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres

Una vez creado y cerrada la termianal si se quiere volver a ejecutar; usar:

sudo docker start BD


## Parametros de conexion a la BD [usuarios]

#--usuario adminsitrador--#
#- Puede gestionar (crear, modificar y elimiar) tablas.
#- Puede leer tablas
#- Puede crear roles

usuario: postgres
contraseña: mysecretpassword

#--usuario solo lectura--#
#- Unicamente puede interrogar tablas (SELECT)

usuario: read_only
contraseña: claveLecturaSegura

## Parametros de conexion a la BD [URL]

url: localhost:5432/postgres
