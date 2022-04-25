#!/bin/bash

# Update heroku's git repo (the BE deployed repo)
git push heroku main
heroku run python manage.py makemigrations
heroku run python manage.py migrate

# Re-seed data
heroku run python manage.py loaddata seed_users.json
heroku run python manage.py loaddata seed_cities.json
heroku run python manage.py loaddata seed_holidays.json
heroku run python manage.py loaddata seed_reviews.json
heroku run python manage.py loaddata seed_followers.json