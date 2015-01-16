==================
iptables-optimizer
==================

Optimize kernel's iptables ruleset by usage.

Author:     Johannes Hubertz <johannes@hubertz.de>

Date:       2015-01-16

Version:    0.9.13

License:    GNU General Public License version 3 or later

Benefit:    Less interrupt load in a statistical point of
            view by minimizing latencies for any 
            IPv4 or IPv6 packets slowed down by very long 
            ip(6)tables chains.

Costs:      Small amount of additional user space workload.

ip6tables-optimizer behaves like iptables-optimizer, except
it uses ip6tables commands instead of iptables commands.

The ip(6)tables-optimizer is intended to sort the chains in
the running Linux-kernel, goal is to reduce latency of
traversing packets. It runs as a shell script, which calls a
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

Using shunit2 tests insure the wrapper part is as reliable
as the python part of the ip(6)tables-optimizer. 
ip(6)tables-optimizer evaluates some line arguments:
-a do not look for /var/cache/iptables-optimizer/auto-apply
-c do not reset packet/byte counters on restoring tables
-h to give this list of valid options
-v add logging, twice shows partition tables in logs
-w shows partition tables for INPUT and OUTPUT only

Starting up the existance of an executable file is checked.

/var/cache/iptables-optimizer/{auto-apply,auto-apply6}

It is fed into the kernel by running ip(6)tables-restore
and afterwards renamed following a simple date-time strategy.
Thats my way of firing new rules into the kernel.

Ideas, suggestions, comments welcome.

Thanks for reading.
Have fun!

Johannes

