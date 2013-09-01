==============================
iptables-optimizer - unittests
==============================

nosetests
---------

The two python classes come along with some unittests. 
A reference-input file is present as it is needed to run the tests.
The prepared nosetests show::

   nostests -v --with-coverage

   Chain_Test: create a chainobject ... ok
   Chain_Test: make partitions from no rules ... ok
   Chain_Test: make partitions from one rule a ... ok
   Chain_Test: make partitions from one rule d ... ok
   Chain_Test: make partitions from one rule r ... ok
   Chain_Test: make partitions from one rule l ... ok
   Chain_Test: make partitions from two rules aa ... ok
   Chain_Test: make partitions from two rules ad ... ok
   Chain_Test: make partitions from five rules adaaa ... ok
   Chain_Test: optimize an empty chainobject ... ok
   Chain_Test: optimize three rules aaa ... ok
   Chain_Test: optimize three rules aar ... ok
   Chain_Test: optimize five rules aalaa ... ok
   Filter_Test: non existant input-file ... ok
   Filter_Test: read reference-input ... ok
   Filter_Test: optimize, check 30 moves and partitions ... ok
   Filter_Test: check output for reference-input ... ok
   
   Name                 Stmts   Miss  Cover   Missing
   --------------------------------------------------
   iptables_optimizer     157      8    95%   232-239
   ----------------------------------------------------------------------
   Ran 17 tests in 0.042s
   
   OK

The missing statements are the following::

   231  if __name__ == "__main__":
   232      try:
   233          f = Filter()
   234          result, msg = f.opti()
   235          sys.stderr.write(msg)  # print partition-table to stderr
   236          outmsg = f.show()
   237          print(outmsg),
   238      except KeyboardInterrupt as err:
   239          print("\rUser stopped, execution terminated")

That's not perfect, but it seems to be sufficient.

tox
---
This is done with the operating systems standard python. For
your convenience, a **tox.ini** is present as well for
tests using different python versions, for now these are
Python.6, 2.7 and 3.2. 

pep 8
-----

tox runs a pep 8 test as well, there are no complains.

Testing is great fun.
