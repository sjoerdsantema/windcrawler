#!/bin/bash

/usr/local/bin/gunicorn windcrawler.wsgi:application --bind "0.0.0.0:$PORT" --env DJANGO_SETTINGS_MODULE=windcrawler.settings.production