# Cuedé

Página con los ejercicios y sus soluciones y discusiones
de las distintas materias de la facu.

Board de Trello para seguir el desarrollo: https://trello.com/b/v9runwuw

## Dependencias

- Docker y docker-compose.
    ```
    sudo apt-get update
    sudo apt-get install docker-compose
    ```

## Corriendo el proyecto

```
sudo docker-compose up --build
```

Esto descarga todas las dependencias necesarias,
corre todas las migraciones, y levanta el servidor en http://localhost:8000/.

### Corriendo los tests

Teniendo el proyecto andando, correr

```
./run_tests.sh
```

Esto se conecta con el container del webserver en `qed_webserver_1` y corre los tests.

### Conectarse a la base de datos de Postgres

```
psql -h localhost -U qed_user -d qed
```

Te va a pedir una contraseña, hay que poner la que está en `docker/database/Dockerfile`.

### Correr un comando en el container del webserver

```
sudo docker ps # Para ver el nombre del container
sudo docker exec -it <nombre de container> /bin/bash # Esto te abre un shell en el container
pipenv shell # Si querés correr comandos usando manage.py
python manage.py createsuperuser # Para crear un usuario en el server
```

## Contribuyendo

Sentite libre de postear un Issue o hacer un Pull Request.
La rama `master` es en donde está la versión actual en
producción, `develop` es donde se hace el desarrollo. Cualquier
Pull Request o cambio debe ser mergeado primero a `develop` y
después a `master` cuando se suba a producción.
