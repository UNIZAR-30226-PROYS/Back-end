
## Docker postgres


Comandos de obtencion
sudo docker pull postgres

sudo docker run --name BD -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres

Una vez creado y cerrada la termianal si se quiere volver a ejecutar; usar:

sudo docker start BD


## Parametros de conexion a la BD

usuario: postgres
contraseña: mysecretpassword
url: localhost:5432/postgres