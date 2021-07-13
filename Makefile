.PHONY: migrate
migrate:
	heroku run python manage.py migrate -a sharknoise-task-manager

.PHONY: venv
venv: .venv
	poetry shell

.PHONY: server
server:
	poetry run python manage.py runserver

.PHONY: static
static:
	poetry run python manage.py collectstatic

.PHONY: newserver
newserver: static server

.PHONY: messages
messages:
	poetry run django-admin makemessages -l ru

.PHONY: translations
translations:
	poetry run django-admin compilemessages

.PHONY: secretkey
secretkey:
	@poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(64))'

requirements.txt: poetry.lock
	poetry export --format requirements.txt --output requirements.txt