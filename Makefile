# Makefile for opti.py, nonsense but needed for dh_make
# so there is nothing real to do, but pleasure

README:
	cat README.txt
	@echo "now running tests"
	@python iptables_optimizer_tests.py
	@rm -rf *.pyc

tests:
	python iptables_optimizer_tests.py

clean:
	@rm -rf *.pyc
