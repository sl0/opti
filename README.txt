=====================
iptables-optimizer.py
=====================

Optimize kernels ruleset by sorting in relation to usage.

Author:     Johannes Hubertz <johannes@hubertz.de>

Date:       2013-07-14

Version:    0.9.2

License:    GNU General Public License version 3 or later

Benefit:    Less interrupt load in a statistical point of
            view, though minimizing latencies for any
            traversing packets.

Costs:      Small amount of additional userspace workload.

The little python script is intended to run on a machine
acting as a paketfilter. It's run by a wrapper (shell),
which itself should be driven by cron every now and then.
Main goal is to have iptables-rules within the chains
sorted by decreasing values of their packet counters.

Of course, the administrators artwok in designing the
rules is untouched, especially the presence of userdefined
chains, reject- or drop-rules is never changed. The only
target are sequences of accept-rules, which are called
partitions inside the script. Within these, there the
rules are sorted. So it should be a challenge for the
administrator to create his rules using as few policy-
changes as possible within his ruleset to have a maximum
benefit of the otimizer-script.

Changes to 0.9.2:
Debianization on the run, multiple corections of path
wrapper now comes as /usr/sbin/iptables-optimizer, the
python as /usr/sbin/iptables_optimizer.py
workfiles now all moved to /var/run, auto-apply still
kept in /root and mentinend in the only kept man-page
iptables-optimizer.8

Changes to 0.9.1:
Now the wrapper is included, see optimize.sh. It can do
auto-apply now. Manuals have been written for both 
optimize.sh and iptables-ptimizer, which is an executable 
copy of iptables_optimizer.py in /sbin. Nosetests are 
replaced by tox, so we're sure about the python part is 
working with python2.6, python2.7 and python3.2 as well 
as compliance to pep8.

Changes to 0.9:
syslog removed, no external commands
Root access is no longer needed for the pyhton-script,
because no external commands are needed any longer.
Instead, use a wrapper outside to read iptables from
kernel into a file and put them back into kernel from
another file, which is created by the wrapper from
stdout of the python-script. So we have a better control
of what happens than ever before. There is no longer
support of auto-apply, because the wrapper can do this
as well if you like it.

There is one single reason for these changes: nosetests
were introduced, about 95% of the code is testet now,
but of course thats no guarantee for no programming
errors. Be careful, look into the code! Look at the
Makefile, tests are called from there. And I agree,
they are right, those rumors about software is broken
by design, if it is not verified by automated tests.
Because this piece of software was broken, but very
rare to be seen. For the tests, an example of input is
included now, see file "reference-input", which is the
default filename for reading.

Changes before: Mostly irrelvant, please have a close
look into the git: https://github.com/sl0/opti.git

Ideas, suggestions, comments welcome.

Thanks for reading.
Have fun!

Johannes

