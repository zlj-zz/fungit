Project = fungit
PY ?= $(shell (python3 -c 'import sys; sys.exit(sys.version < "3.6")' && \
	      which python3) )

ifeq ($(PY),)
  $(error No suitable python found(>=3.7).)
endif

.PHONY: test
test:
	$(PY) ./tests/test_run.py

.PHONY: lint
lint:
	@if [ ! -f flake8 ]; then $(PY) -m pip install flake8; fi
	@flake8 --ignore=E501,E402

.PHONY: del
del:
	@if [ -d ./dist ]; then rm -r ./dist/; fi
	@if [ -d ./build ]; then rm -r ./build; fi
	@if [ -d ./$(Project).egg-info ]; then rm -r "./$(Project).egg-info"; fi

.PHONY: release
release: del
	$(PY) setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: install
install: del
	$(PY) setup.py install

.PHONY: clean
clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
