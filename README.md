# QED

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
corre todas las migraciones, y levanta el servidor en http://127.0.0.1:8000/.

## Contribuyendo

Sentite libre de postear un Issue o hacer un Pull Request.
La rama `master` es en donde está la versión actual en
producción, `develop` es donde se hace el desarrollo. Cualquier
Pull Request o cambio debe ser mergeado primero a `develop` y
después a `master` cuando se suba a producción.
