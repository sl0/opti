iptables-optimizer - intro
==========================

In many SMB environments long term running packet filters are quite normal. 
Usually the administrators are often asked to add a rule for a special purpose, 
but only accidentally are kept informed about the end of life for the 
needs. So the set of rules grows over time. Organizational rules may try to
minimize this bad behavior, but nevertheless it is the normal way of doing.

Now assume you have a filtering Linux router with some thousands iptables
rules in its filtering chains. Unfortunately these this will produce 
latency for every traversing packet. And of course, this latency is 
unwanted behavior. The only useful way of improving is to reduce the 
length of the chains. Buts that is not easy if ever possible. Usually 
nobody is responsible enough to say, this special rule is no longer 
needed. You would like to know somebody for every rule. 

One of the first ideas for an optimization was to use the counters on each
rule to see, if it is needed at all. The set of rules should run for a month 
and all those rules showing zero usage could be deleted. Sounds easy, but 
this is not as simple doing as said. Initial step to a solution was to
add the beautiful comment module in every iptables-command and a number
from the corresponding source of the rule. So it was easy to identify
the iptables-command within the source. Nevertheless the finding of
useless rules was not done because some lack of time. The latency grew.

Another idea came up: partitioning of the long chains into parts of same
targets. Within a partition the rules might be sorted on behalf of the 
packet counters so that the most often rules are searched first. And all 
the unused rules wouldn't be consulted so much often. Sounds crazy, but 
seemed to be `plausible <plausible.html>`_. Tests were done, python was chosen for the 
programming part of the job. And a long and stony way started with the 
first step.

shell wrapper
-------------

The shell wrapper simply acts in few steps: 

  1. If ``ref-with-error-in`` exists, exit immediately due to error of previous run
  2. If the administrator has spend a new rule set in ``auto-apply``, restore it into the kernel, rename, exit
  3. Use **iptables-save -t filter -c** to store the kernels tables to a file ``reference-input``
  4. Run iptables_optimizer.py, save stdout to ``reference-output``, stderr to ``iptables-optimizer-partitions``
  5. Use **iptables-restore** to push the modified content in ``reference-output`` back to the kernel
  6. If called with an argument, use **logger** to put ``iptables-optimizer-partitions`` into syslog

Some error-checking is done, so it is a little bit longer 
than four lines of code. The real tricky things are done at step 3, following. In case of an error,
reference-input is renamed to ``ref-with-error-in``, which existance is checked on startup and exit. 
So further runs are not doing any harm after a first error.

Some Debian conventions about the path for the files are respected:

+---------------------------------------------------------+
|  ``Path``                                               |
+=========================================================+
|  ``/usr/sbin/iptables-optimizer``                       |
+---------------------------------------------------------+
|  ``/usr/share/man/man8/iptables-optimizer.8.gz``        |
+---------------------------------------------------------+
|  ``/usr/share/pyshared/iptables_optimizer.py``          |
+---------------------------------------------------------+
|  ``/var/cache/iptables-optimizer/auto-apply``           |
+---------------------------------------------------------+
|  ``/var/cache/iptables-optimizer/auto-apply-YYYYMMDD``  |
+---------------------------------------------------------+
|  ``/var/run/{reference-input,ref-with-error-in}``       |
+---------------------------------------------------------+
|  ``/var/run/{reference-output,ref-with-error-out}``     |
+---------------------------------------------------------+
|  ``/var/run/iptables-optimizer-partitions``             |
+---------------------------------------------------------+
|  ``/var/run/iptables-optimizer-last-run``               |
+---------------------------------------------------------+


python code
-----------

Python comes with batteries included, they say. The subprocess module
can execute every shell command from within the python code. Sounds well,
worked well until --- sometimes you have some different python versions
running because of different operating systems, f.e. in Debian systems
you may find python 2.5, 2.6, 2.7 and 3.2, as they are distributed as
standard versions in etch, Lenny, squeeze and wheezy. Surprisingly the
subprocess behavior changed a lot in these. I was very frustrated
about that and therefore I decided not to use it. Benefit was to have 
a single python script containing the necessary stuff without calling 
external commands, but running well in all different python versions. 
The external parts were migrated to an external shell script, which 
itself calls the python snippet for the complex actions now.

So, what needs to be done? The filter tables are search for every
traversing packet, all the rules are checked for matching, and if 
one matches, its target is applied to the packet and usually the
action for this packet is finished. The less rules must be searched
the quicker the packet is forwarded or dropped. So the rules should
be assorted in a way, more often used ones should be found quicker
than those which are seldom used. But, there is a handicap: Perhaps
the administrator wants some special packets to be dropped and some
other to be forwarded. The old-fashioned handmade rule set respects
this, and the administrators artwork shall never be destroyed by
sorting. Let's think again, is it possible to sort the rules and to
respect his artwork? Yes, it is possible, but few restrictions apply.

In every chain we have some rules to accept, some to drop and some 
others, each intermixed with the others. Partitions are the key to
those which may be sorted without affecting the overall policy. If 
we group some consecutive rules having the same targets, we can
exchange them without changing the policy. Sure.

Two python classes were build: Chain and Filter. An instance of the
Filter class holds at least the predefined chains, perhaps some
user defined chains. On creation it reads the given file.

More in `unittests <unittests.html>`_ are fine

#`configuration <config.html>`_
