==========================
iptables-optimizer - intro
==========================

In many SMB environments long term running packet filters are quite
normal. Usually the administrators are often asked to add a rule for
a special purpose, but only accidentally are kept informed about the
end of life for the needs. So the set of rules grows over long time.
Organizational rules may try to minimize this bad behavior, but
nevertheless it is the normal way of doing.

Assume you have a filtering Linux router with some thousands of
iptables rules in its iptables chains. Unfortunately these this will
produce latency for every traversing packet. And of course, this
latency is unwanted behavior. The only useful way of improving is to
reduce the length of the chains. Buts that is not easy if ever
possible. Usually nobody is responsible enough to say, this special
rule is no longer needed. You would like to know somebody for every
rule.

One of the first ideas for an optimization was to use the counters
on each rule to see, if it is needed at all. The set of rules should
run for a month and all those rules showing zero usage could be
deleted. Sounds easy, but this is not as simple doing as said.
Initial step to a solution was to add the beautiful comment module
in every iptables-command and a number from the corresponding source
of the rule. So it was easy to identify the iptables-command within
the source. Nevertheless the finding of useless rules was not done
because some lack of time. The latency grew.


Another idea came up: partitioning of the long chains into parts of same
targets. Within a partition the rules might be sorted on behalf of the
packet counters so that the most often rules are searched first. And all
the unused rules wouldn't be consulted so much often. Sounds crazy, but
seemed to be `plausible <plausible.html>`_. Tests were done, python was
chosen for the programming part of the job. And a long and stony way
started with the first step.

shell wrapper
=============

As IPv6 is coming soon, a simple modification in the wrappers source led to
ip6tables-optimizer, which behaves exactly the same as iptables-optimizer...
So the shell wrapper exists in two versions now, the second is symlinked to
the first file.

The shell wrapper simply acts in four steps after evaluating the options:

  1. If an executable file ``/var/cache/iptables-optimizer/auto-apply`` exists, restore it into the kernel and rename it

  2. Use ``iptables-save -t filter -c`` to store the kernels tables into a file

  3. Run ``iptables_optimizer.py``, save stdout and stderr for errorchecking

  4. Use ``iptables-restore`` to push back the rules into the kernel

Some error-checking is done, so the code is a little bit more than four lines.
In case of an error, the shell wrapper exits immediately due to runnig with ``bash -e``.
The ``pipefail`` option ensures failures to be seen in piped commands as well.
The real tricky things are done in the pythonic part.

Some command line options are provided::

-a    do not evaluate auto-apply (auto-apply6)
-c    keep the packet/byte counters on restoring
-h    help message about valid options and exit 1
-v    verbose logging about the steps. If given twice, partitions and moves are logged
-w    logging partiontions and moves for INPUT and OUTPUT chains only, implies -vv,


Usually the iptables-optimizer exits with a return value of zero indicating no error.
The debian packaging produces two files for dpkg::

   iptables-optimizer_x.y.z-v.deb
   iptables-optimizer-doc_x.y.z-v.deb

For production environment the documents are not needed, for your understanding
you do not need the binary package at all.

All used functions within the shell wrapper are sourced from another file,
``iptables-optimizer-functions``. This seems to be useful for making them testable
with Karen Wards shunit2, which is available as free software.


python code
===========

The only reason to have a shell wrapper for the python script was found in
different python versions, which treated the subprocess module very different
in different Debian stable versions from lenny to jessie.

Python comes with batteries included, they say. The subprocess module
can execute every shell command from within the python code. Sounds well,
worked well until --- sometimes you have some different python versions
running because of different operating systems, f.e. in Debian systems
you may find python 2.5, 2.6, 2.7 and 3.2, 3.3 and 3.4, just like they
are distributed as standard versions in etch, Lenny, squeeze and wheezy.
Surprisingly the subprocess behavior changed a lot in these. I was very
frustrated about that and therefore decided not to use it. Benefit was
to have a single python script containing the necessary stuff without calling
external commands, but running well in all different python versions.
The external parts were migrated to an external shell script, which
itself calls the python snippet for the complex actions now.

So, what needs to be done? The filter tables are searched for every
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
others, each intermixed with the others. From a mathematical point
of view (set theory) partitions are the key to solve the puzzle. If
we group consecutive rules having the same targets, inside these groups
we can exchange the rule without changing the policy. Sure.

So we have to find partition borders and then sort within each partition
on behalf of the packet counters.

Two python classes were build: Chain and Filter. An instance of the
Filter class holds at least the predefined chains, perhaps some
user defined chains. On creation of an instance it reads the given
file.

Fortunately the python code is completely independant of the rules
content as it only evaluates the packet/byte counters. So it is used
in the iptables-optimizer as well as in the ip6tables-optimizer.


class Filter
------------

Instanciating the Filter class reads a file, which is an output of
``iptables-save -c``, so we get the chain names at first and then
their content. For each chain an instance of the class Chain is
set up. The packet counters are needed, this is done by the "-c" in the
2nd step of the wrapper. The init method ends up with a full
representation of the kernels filter tables in memory.

The opti method uses the opti method of all chain instances, the show
method is just a wrapper around the many print statements for testing
purposes and for better separating any additional information such
as statistics, which then are printed out to stderr. This kind
separation is fine, especially within the shell wrapper.


class Chain
-----------

On reading the file, an instance of the Chain class is build on the fly.
The appends are done using the corresponding append method, and so
at last a complete picture of the kernels view is in memory. The opti
method on startup uses the make_partitions method prior to the sorting
related to the packet counters.


