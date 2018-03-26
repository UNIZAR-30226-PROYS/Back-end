
## Docker

Para usar el servidor localmente con Docker, abre una terminal en este directorio y ejecuta:

```bash
# building the image
docker build -t swagger_server .

# starting up a container
docker run -p 8080:8080 swagger_server
```

A continuación abre un navegador y entra a la dirección `localhost:8080/api/ui`, donde podrás ver todos los endpoints y métodos disponibles, y ejecutar llamadas de prueba a la API.

A la hora de construir las llamadas a la API hay que usar el path `localhost:8080/api/`. Si, por ejemplo, se quiere usar el endpoint `/users/123/follow`, hay que hacer una llamada a `localhost:8080/api/users/123/follow`.
