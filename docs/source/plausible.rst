Plausibilty
===========


Initial Scenario
----------------

Assume the following single chain as part of a NetFilter table:

+-----+------+----------+------+
|  No | pkts |  target  | part |
+=====+======+==========+======+
|  1  |   15 |  accept  |  1   |
+-----+------+----------+------+
|  2  |   18 |  accept  |  1   |
+-----+------+----------+------+
|  3  |  119 |  accept  |  1   |
+-----+------+----------+------+
|  4  |   21 |  drop    |  2   |
+-----+------+----------+------+
|  5  |   30 |  accept  |  3   |
+-----+------+----------+------+
|  6  |   36 |  accept  |  3   |
+-----+------+----------+------+
|  7  |    1 | userdef1 |  4   |
+-----+------+----------+------+
|  8  |    5 | userdef2 |  5   |
+-----+------+----------+------+
|  9  |    6 |  drop    |  6   |
+-----+------+----------+------+
| 10  |    6 |  drop    |  6   |
+-----+------+----------+------+

Regarding this chain, we see rule 3 is more often used than rule 1 and rule 2.
Administrators artwok consists of 6 partitions, of course this is his implicit 
knowledge about his security policy, which is never seen nor explained in the 
kernel. There we only see some tables and their content.

Exchange example
----------------

So what happens, if we change the sequence of the rules by respecting the
partitioning, the administrator wanted to the following scenario, i.e. 
rule 3 is positioned now on top, the former rules 1 and 2 are in postition 2 and 3 now,
rule 5 and 6 were swapped:

+-----+------+----------+------+
|  No | pkts |  target  | part |
+=====+======+==========+======+
|  3  |  119 |  accept  |  1   |
+-----+------+----------+------+
|  2  |   18 |  accept  |  1   |
+-----+------+----------+------+
|  1  |   15 |  accept  |  1   |
+-----+------+----------+------+
|  4  |   21 |  drop    |  2   |
+-----+------+----------+------+
|  6  |   36 |  accept  |  3   |
+-----+------+----------+------+
|  5  |   30 |  accept  |  3   |
+-----+------+----------+------+
|  7  |    1 | userdef1 |  4   |
+-----+------+----------+------+
|  8  |    5 | userdef2 |  5   |
+-----+------+----------+------+
|  9  |    6 |  drop    |  6   |
+-----+------+----------+------+
| 10  |    6 |  drop    |  6   |
+-----+------+----------+------+

From the policy view, nothing has changed. Packets may pass as before or are dropped as before.
But the kernel now finds the more often rule 3 quicker than in the initial setup. 

Conclusion
----------

Thats exactly
what was intended by the swapping. The length of the partitions isnot changed, for less
latency the administrator should try to build as less partitions as possible. Exactly that is
his artwork and no optimizer or other autmatism can help him thereby.

