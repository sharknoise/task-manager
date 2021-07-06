secretkey:
	@poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(64))'

requirements.txt: poetry.lock
	@poetry export --format requirements.txt --output requirements.txt

.PHONY: secretkey