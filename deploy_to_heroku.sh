#!/bin/bash

git add .
git commit -m "automated commit for redeployment"
git push heroku main
heroku run python manage.py makemigrations
heroku run python manage.py migrate