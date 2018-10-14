# QED

Página con los ejercicios y sus soluciones y discusiones
de las distintas materias de la facu.

Board de Trello para seguir el desarrollo: https://trello.com/b/v9runwuw

## Dependencias

- `pipenv`: https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv
- `PostgreSQL`:

    ```
    sudo apt-get update
    sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
    ```

## Configurar el proyecto

### Configurar la base de datos de PostgreSQL

Se necesita crear una base de datos llamada `qed`
con el dueño de nombre `qed_user` y password `PWD-.,`.
Los pasos para hacer esto son:

1. Abrir la CLI de postgres:
    ```
    $ psql
    ```
    Si no te deja entrar diciendo que el usuario no está permitido,
    quizá tengas que hacer un `sudo su - postgres` antes para usar
    el usuario `postgres`.

2. Crear el usuario:
    ```
    > CREATE USER qed_user WITH PASSWORD 'PWD-.,';
    ```
3. Crear la base de datos:
    ```
    > CREATE DATABASE qed WITH OWNER qed_user;
    ```

Unos buenos tutoriales de cómo instalar postgres y hacer estos
pasos en Windows, Mac y Linux son [este](https://tutorial-extensions.djangogirls.org/en/optional_postgresql_installation/) y [este](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04).


### Siguientes pasos
En el directorio del proyecto:
```
$ pipenv install              # Instalar dependencias de pip
$ pipenv shell                # Entrar al virtualenv
$ cd secomplican/
$ python3 manage.py migrate   # Migrar la base de datos
$ python3 manage.py runserver # Iniciar el servidor
```

Y listo! Ahora podés entrar a la URL http://127.0.0.1:8000/ y
ver el servidor andando.
