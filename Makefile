# Makefile for opti.py, now needed for senseful tests
# so there is nothing real to do, but pleasure

testing:
	@more README.txt
	@echo "Now starting tests ..."
	/usr/local/bin/tox

clean:
	@python setup.py clean --bdist-base build
	@rm -rf .coverage *.pyc reference-output rs ts build
