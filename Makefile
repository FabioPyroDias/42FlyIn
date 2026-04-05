PIP_INSTALL = flyin/bin/pip install
PYTHON = flyin/bin/python3

MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

RM = rm -rf

install:
	python3 -m venv flyin
	$(PIP_INSTALL) --upgrade pip
	$(PIP_INSTALL) flake8
	$(PIP_INSTALL) mypy

run:

debug:
	$(PYTHON) -m pdb ######################################TODO

clean:

lint:
	$(PYTHON) flake8
	$(PYTHON) mypy $(MYPY_FLAGS)

lint-strict:
	$(PYTHON) flake8
	$(PYTHON) mypy --strict