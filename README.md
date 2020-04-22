# Cuedé

**https://cuede.herokuapp.com**

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
sudo docker-compose up
```

Esto descarga todas las dependencias necesarias,
corre todas las migraciones, y levanta el servidor en http://localhost:8000/.

### Corriendo los tests

Teniendo el proyecto andando, correr

```
./run_tests.sh
```

Esto se conecta con el container del webserver en `cuede_webserver_1` y corre los tests.

### Correr un comando en uno de los containers

```
sudo docker ps # Para ver el nombre del container, por ejemplo, cuede_webserver_1
sudo docker exec -it <nombre de container> /bin/bash # Esto te abre un shell en el container
cd src/ && python manage.py createsuperuser # Para crear un usuario en el server, por ejemplo
```

### Conectarse a la base de datos de Postgres

Primero, abrir un shell en el container de la base de datos (en general va a ser cuede_database_1) y después correr

```
psql -h localhost -U qed_user -d qed
```

Eso te va a abrir una consola de PostgreSQL en la que podés tirar queries a la base de datos.

## Contribuyendo

Sentite libre de postear un Issue o hacer un Pull Request.
La rama `master` es en donde está la versión actual en
producción, `develop` es donde se hace el desarrollo. Cualquier
Pull Request o cambio debe ser mergeado primero a `develop` y
después a `master` cuando se suba a producción.
