#!/usr/bin/env bash
sudo docker exec -it qed_webserver_1 pipenv run bash -c 'cd secomplican && python manage.py test'