# QED

Página con los ejercicios y sus soluciones y discusiones
de las distintas materias de la facu.

Board de Trello para seguir el desarrollo: https://trello.com/b/v9runwuw

## Dependencias

- pipenv
- postgresql

## Para correr

```
$ pipenv install
$ pipenv shell
$ cd secomplican/
$ python manage.py migrate # Debería romper acá, porque tenés que inicializar la base de datos de postgres.
$ python manage.py runserver
```