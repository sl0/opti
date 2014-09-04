==================
iptables-optimizer
==================

Optimize kernels ruleset by sorting in relation to usage.

Author:     Johannes Hubertz <johannes@hubertz.de>

Date:       2014-09-04

Version:    0.9.11

License:    GNU General Public License version 3 or later

Benefit:    Less interrupt load in a statistical point of
            view, though minimizing latencies for any
            traversing packets.

Costs:      Small amount of additional user space workload.

The iptables-optimizer is intended to sort the chains in
the running Linux-kernel, goal is to reduce latency of
throughput. It runs as a shell script, which calls a
python script. This sorts the chains by decreasing values
of packet counters, afterwards the result is restored into
the kernel.
Of course, the administrators artwork in designing the
rules is untouched, especially the presence of user defined
chains, reject- or drop-rules is never changed. The only
target are sequences of accept-rules, which are called
partitions inside the script. Within these, there the
rules are sorted. So it should be a challenge for the
administrator to create his rules using as few policy-
changes as possible within his ruleset to have a maximum
benefit of the optimizer-script.

Changes to 0.9.11:
Introduced ip6tables-optimizer by creating a symlink and
minor changes within the wrapper. The manpage for the new
ip6tables-optimizer is created by replacing iptables- with
ip6tables with sed.

Changes to 0.9.10:
The shell wrapper was completely rewritten. Using shunit2
tests have been written to make the wrapper as reliable
as the python part of the iptables-optimizer. Some command
line arguments are evaluated:
-a do not look for /var/cache/iptables-optimizer/auto-apply
-c do not reset paket/byte counters on restoring tables
-v add logging, twice shows partition tables
-w shows partition tables for INPUT and OUTPUT only

A small modification on the iptables_optimizer.py: As an
command line argument it accepts a filename for reading now.

Changes to 0.9.9:
Debian package now ships a single python file, no more
any python3 dependencies as python2 is standard in Debian
deb-helpers for building python-modules removed, default
python from distribution is used in shebang directly

Changes to 0.9.8:
iptables_optimizer.py is now python3.2 ready and
tested by tox with nosetests3

Changes to 0.9.7:
Keeping pylint happy is an unreached goal. setuptools for
setup, version step.

Changes to 0.9.6:
no need of postinst, auto-apply is fetched from
/var/cache/iptables-optimizer now

Changes to 0.9.5:
Version numbers corrected in setup.py, README.txt, and in
the scripts. postinst now contains #DEBHELPER# tag for
silence with gpb buildpackage --git-pbuilder

Changes to 0.9.4:
/root/auto-apply moved to /var/cache/auto-apply/auto-apply
postinst creates /var/cache/auto-apply/
i-o.py moved to /usr/share/pyshared/iptables_optimizer.py
man-page adapted and more verbose now.

Changes to 0.9.3:
/root/auto-apply moved to new location:
/var/cache/auto-apply/auto-apply
debian/postinst written

Changes to 0.9.3:
Package name changed to iptables-optimizer
No longer calls of non-shipped elements

Changes to 0.9.2:
Debianization on the run, multiple corrections of path
wrapper now comes as /usr/sbin/iptables-optimizer, the
python as /usr/sbin/iptables_optimizer.py
workfiles now all moved to /var/run, auto-apply still
kept in /root and mentioned in the only kept man-page
iptables-optimizer.8

Changes to 0.9.1:
Now the wrapper is included, see optimize.sh. It can do
auto-apply now. Manuals have been written for both
optimize.sh and iptables-optimizer, which is an executable
copy of iptables_optimizer.py in /sbin. Nosetests are
replaced by tox, so we're sure about the python part is
working with python2.6, python2.7 and python3.2 as well
as compliance to pep8.

Changes to 0.9:
syslog removed, no external commands
Root access is no longer needed for the python-script,
because no external commands are needed any longer.
Instead, use a wrapper outside to read iptables from
kernel into a file and put them back into kernel from
another file, which is created by the wrapper from
stdout of the python-script. So we have a better control
of what happens than ever before. There is no longer
support of auto-apply, because the wrapper can do this
as well if you like it.

There is one single reason for these changes: nosetests
were introduced, about 95% of the code is tested now,
but of course thats no guarantee for no programming
errors. Be careful, look into the code! Look at the
Makefile, tests are called from there. And I agree,
they are right, those rumors about software is broken
by design, if it is not verified by automated tests.
Because this piece of software was broken, but very
rare to be seen. For the tests, an example of input is
included now, see file "reference-input", which is the
default filename for reading.

Changes before: Mostly irrelevant, please have a close
look into the git: https://github.com/sl0/opti.git

Ideas, suggestions, comments welcome.

Thanks for reading.
Have fun!

Johannes

