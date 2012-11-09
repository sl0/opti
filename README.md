=======
opti.py
=======

iptables-runtime-optimizer
==========================

Author:     sl0.self@googlemail.com

Date:       2012-11-09

Version:    0.2

License:    GNU General Public License version 3 or later



This little python script is intended to run on a paketfilter-machine
running on any actual linux distribution. As cpu-load increases due to 
number of rules and traffic, it might be a good idea to sort the rules
in runtime due to their usage, represented by paket-counters.

Of course, the administrators artwok in designing the rules is untouched,
especially the presence of userdefined chains, reject- or drop-rules is
never changed. The only target are sequences of accept-rules, which are
called partitions inside the script. Within these, there the rules are
sortet. So it should be a challenge for the administrator to create his
rules using as few policy-changes as possible within his ruleset to have 
a maximum benefit of the otimizer-script.

And as usual, the script must be run as root, which is neccessary for
any iptables-commands. Used system commands are:

iptables-save -t filter -c
iptables -A  (first inserting a lower rule into a higher position)
iptables -D  (then deleting the lower rule, which is not used any longer)
So the number of rules keeps constant.

The python code automatically works on all chains within the filter-group.

For now, there are no doctests or unittests. If there is some time, they
will come.

Ideas, suggestions, comments welcome.

Thanks for reading.
Have fun!

sl0

