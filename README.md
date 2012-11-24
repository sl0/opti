=======
opti.py
=======

iptables-runtime-optimizer
==========================

Author:     sl0.self@googlemail.com

Date:       2012-11-23

Version:    0.4

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

And as usual, the script must be run as root, which is neccessary for
any iptables-commands. Used system commands are:

iptables-save -t filter -c

iptables -A  (first inserting a lower rule into a higher position)

iptables -D  (then deleting the lower rule, which is not used any longer)

iptables -Z  (just the before long sleep command, counters are reset)

sleep        (sort is ready now visible in process-list)

The later two are new within version 0.3, counter-reset gives the chance,
to have an sorted ruleset of current traffic, not on todays traffic. The
sleep command now is called externally although the internal command works 
well, because it's useful to have an idea of internal state from the 
outside.

Version 0.4 relies on python 2.6 due to some crashes seen with 
python 2.7.3rc2, which is delivered within Debian wheezy for now.
Using version 2.6 the iptables-optimizer seems to run stable.
Now some minimal errorchecking is done by evaluation of the iptables
returncode, but still there is no logging to syslog or the like. 
Of course, stdout might be redirected to some file for later revisions.
Seeing the first non-zero returncode, the iptables-optimizer exits.

The number of rules keeps constant. The python code automatically works 
on all chains within the filter-group.

For now, there are no doctests or unittests. If there is some time, they
will come. Internally there is still need of some error-checking, especially
on the iptables -A command. If that one fails, the ruleset lenght will be 
decreased by one and the rule will be missing after the -D, ugly ...

Ideas, suggestions, comments welcome.

Thanks for reading.
Have fun!

sl0

