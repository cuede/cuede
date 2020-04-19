#!/usr/bin/env bash
sudo docker exec -it cuede_webserver_1 pipenv run bash -c 'cd src && python manage.py test'