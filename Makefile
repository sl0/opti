# Makefile for opti.py, now needed for senseful tests
# so there is nothing real to do, but pleasure

testing:
	@cat README.txt
	@echo "Now starting tests ..."
	/usr/local/bin/tox

rpm:
	python setup.py bdist_rpm

deb:
	gbp buildpackage --git-pbuilder

clean:
	@python setup.py clean --bdist-base build
	@rm -rf .coverage *.pyc reference-output rs ts build
	@rm -rf __pycache__ iptables_optimizer.egg-info/ dist
	@rm -rf *.py3
