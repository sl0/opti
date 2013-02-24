=====================
iptables-optimizer.py
=====================

Optimize kernels ruleset by sorting in relation to usage
Goal is to have less interrupt load in a statistical point of view

Author:     sl0.self@googlemail.com

Date:       2013-02-24

Version:    0.9

License:    GNU General Public License version 3 or later



This little python script is intended to run on a paketfilter-machine
running on any actual linux distribution. As cpu-load increases due to 
number of rules and traffic, it might be a good idea to sort the rules
in runtime due to their usage, represented by paket-counters.

Of course, the administrators artwok in designing the rules is untouched,
especially the presence of userdefined chains, reject- or drop-rules is
never changed. The only target are sequences of accept-rules, which are
called partitions inside the script. Within these, there the rules are
sorted. So it should be a challenge for the administrator to create his
rules using as few policy-changes as possible within his ruleset to have 
a maximum benefit of the otimizer-script.

Major changes were done from 0.8 to 0.9:
syslog removed, no external commands

As of version 0.9, all root access is no longer needed for the pyhton-
script, because no external commands are needed any longer. Instead, use
a wrapper outside to read iptables from kernel into a file and put them
back into kernel from another file, which is created by the wrapper from
stdout of the python-script. So you may have a better control of what
happens than ever before. There is no longer support of auto-apply, because
the wrapper can do this as well if you like it.

There is one single reason for these changes: nosetests were introduced, 
about 95% of the code is testet now, but of course thats no guarantee for no 
programming errors. Be careful, look into the code! Look at the Makefile,
tests are called from there. And I agree, they are right, those rumors about 
software is broken by design, if it is not verified by automated tests.
Because this was broken, but very rare to be seen. For the tests, an
example of input is included now, see file "reference-input", which is the 
default filename for reading.

The wrapper may look rather simple:
-------------------------------------------------------------------
#/bin/sh

# read actual tables _with_ counters
iptables-save -c > reference-input

# sort the rules
python iptables-optimizer.py > reference-output

# write them back to kernel without counter-values
iptables-restore < reference-output

exit 0
-------------------------------------------------------------------

Of course, you may wish to improve the wrapper for your needs. 
How often it runs, perhaps best may be decided by cron.

Ideas, suggestions, comments welcome.

Thanks for reading.
Have fun!

sl0

