secretkey:
	@poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(64))'

.PHONY: secretkey