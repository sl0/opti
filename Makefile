# Makefile for opti.py, now needed for senseful tests
# so there is nothing real to do, but pleasure

README:
	@cat README.txt
	@echo "Now starting tests:\n"
	@nosetests -v --with-coverage  iptables_optimizer_tests.py
	@rm -f *.pyc

tests:
	@sort -g reference-input > rs
	@python iptables_optimizer.py |tee reference-output | sort -g > ts
	@diff rs ts || /bin/true

clean:
	@rm -rf .coverage *.pyc reference-output rs ts
