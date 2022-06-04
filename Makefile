install: requirements.in
	pip install -U pip pip-tools wheel setuptools
	pip-sync

compile:
	pip-compile

run: install
	python main.py