iptables-optimizer intro
========================

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
seemed to be plausible. Tests were done, python was chosen for the 
programming part of the job. And a long and stony way started with the 
first step.


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


shell wrapper
-------------

