# Makefile for opti.py, now needed for senseful tests
# so there is nothing real to do, but pleasure

alltests:
	@make shelltests testing

shelltests:
	bash iptables-optimizer-tests.sh
	bash ip6tables-optimizer-tests.sh

testing:
	/usr/bin/tox

rpm:
	python3 setup.py bdist_rpm

deb:
	gbp buildpackage --git-pbuilder

doc:
	make -C docs html

clean:
	make -C docs clean
	@python setup.py clean --bdist-base build
	@rm -rf .coverage *.pyc reference-output rs ts build
	@rm -rf __pycache__ iptables_optimizer.egg-info/ dist
	@rm -rf *.py3 .tox .noseids .pybuild
	@dh_clean || /bin/true

