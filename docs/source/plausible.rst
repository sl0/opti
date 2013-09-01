Plausibility
============


Initial Scenario
----------------

Assume the following single chain as part of a NetFilter table, the number and the partition number rows 
are meta information and not taken from or represented in the kernel.
(only meaningful content is shown here):

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

Partitions
----------

Partitions are assigned to the rules regarding their targets, 
starting with the first rule and the target accept. Rule 4 has 
another target, so rule 1, 2 and 3 build the first partition, 
the second partition starts with rule 4 and ends with it, 
because rule 5 has another target, so we continue until the 
end of the chain. At last we have found the partition table as 
a list::

   partition numbers  1       2       3       4       5       6 
   partition list = [[1, 3], [4, 4], [5, 6], [7, 7], [8, 8], [9, 10], ]

The list is constructed from elements, a two element list each. Every single element is build from the starting and ending
number of the rules having the same target and an implicit length, which is easily calculated as::

   length = 1 + end - start

Viewed as a table it looks like:

+-------------+-----------+----------+-------------+
| ``Part.No`` | ``Start`` |  ``End`` |  ``Length`` |
+=============+===========+==========+=============+
|     ``1``   |     ``1`` |    ``3`` |      ``3``  |
+-------------+-----------+----------+-------------+
|     ``2``   |     ``4`` |    ``4`` |      ``1``  |
+-------------+-----------+----------+-------------+
|     ``3``   |     ``5`` |    ``6`` |      ``2``  |
+-------------+-----------+----------+-------------+
|     ``4``   |     ``7`` |    ``7`` |      ``1``  |
+-------------+-----------+----------+-------------+
|     ``5``   |     ``8`` |    ``8`` |      ``1``  |
+-------------+-----------+----------+-------------+
|     ``6``   |     ``9`` |   ``10`` |      ``2``  |
+-------------+-----------+----------+-------------+

Now lets concentrate on the first partition and the rules in it:

+-----+------+----------+------+
|  1  |   15 |  accept  |  1   |
+-----+------+----------+------+
|  2  |   18 |  accept  |  1   |
+-----+------+----------+------+
|  3  |  119 |  accept  |  1   |
+-----+------+----------+------+

We see, some (perhaps) different things shall be accepted by these 
three filter rules. So if a packet matches one of them or more, it 
is accepted. If it matches the third rule, the two before are 
consulted for nothing. Is the overall policy affected, if we change 
the position of the third rule to the top position? The answer is 
no, because the accepted traffic in sum is exactly the same 
regarding this partition of the complete rule set. So we can 
rearrange it to:

+-----+------+----------+------+
|  3  |  119 |  accept  |  1   |
+-----+------+----------+------+
|  2  |   18 |  accept  |  1   |
+-----+------+----------+------+
|  1  |   15 |  accept  |  1   |
+-----+------+----------+------+

As a result, the packets allowed by the now first rule are passed quicker because
the other to rules are not taken into account. *Latency is reduced.*

Partitions with a length of one are of no interest, surprisingly. Their
content and their position are static all over the time.


Exchanged rules
---------------

Working down the partitions list, we come to this final result for the chain,
the rule numbers are kept from the example shown above:

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
But the kernel now finds the more often used rules quicker than before.

Conclusion
----------

That is exactly what was intended by the swapping. The length of the partitions is not changed, 
for less latency the administrator should try to build as less partitions as possible. Exactly that is
his artwork and no optimizer nor any other automatism can help him to solve this puzzle.

How often shall this calculation be done? You have to find out yourself on your behalf.
When I wrote the python code, it was run by cron every second on a dual core system and reducing
latency for every end users joy.
