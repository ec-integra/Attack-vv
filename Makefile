integration_tests:
	pytest --cov-report term-missing --cov=. tests/integration/

unit_tests:
	pytest --cov-report term-missing --cov=. tests/unit/

all_tests:
	pytest --cov-report term-missing --cov=. tests/

check_pep:
	flake8 ./