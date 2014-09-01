=======================================
iptables_optimizer_tests.py - unittests
=======================================

nosetests
---------

The two python classes come along with some unittests. 
A reference-input file is present as it is needed to run the tests.
The prepared nosetests show like this::

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
   iptables_optimizer     167     15    91%   33-34, 162-163, 236-246
   ----------------------------------------------------------------------
   Ran 17 tests in 0.048s

   OK

The missing statements are the following::

    33    except:
    34        pass    # python2.6

   162        except:
   163            self.chains        = {}    # python2.6

   236    file_to_read = "reference-input"
   237    if len(sys.argv)       > 1:
   238        file_to_read = sys.argv[1]
   239    try:
   240                 f = Filter(filename=file_to_read)
   241        result, msg = f    .opti()
   242        sys.stderr.write(msg)  # print partition-table t    o stderr
   243        outmsg = f.show()
   244        print(outmsg),        
   245    except KeyboardInterrupt as err:
   246        print("\rUs     er stopped, execution terminated")
                                                                    

That's not perfect, but it seems to be sufficient.

tox
---
This is done with the operating systems standard python. For
your convenience, a **tox.ini** is present as well for
tests using different python versions, for now these are
Python2.7 and Python3.4 which are used in debian jessie.

pep 8
-----

tox runs a pep 8 test as well, there are no complains.

Testing is great fun.
