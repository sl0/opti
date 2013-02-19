#!/usr/bin/env python

#encoding:utf8

from iptables_optimizer import extract_pkt_cntr, Chain, Filter
import unittest

class ChainTest(unittest.TestCase):
    '''tests for class Chain'''

    def test_first_chain(self):
        c = Chain("FIRST_CHAIN")
        self.assertEquals("FIRST_CHAIN", c.name)
        self.assertEquals([], c.liste)
        self.assertEquals([], c.cntrs)
        self.assertEquals([], c.bytes)
        self.assertEquals([], c.partitions)
        self.assertEquals(0, c.make_partitions())
        self.assertEquals([], c.partitions)

    def test_second_chain(self):
        c = Chain("INPUT")
        self.assertEquals("INPUT", c.name)
        line = '[9:10] -A INPUT -p tcp -m tcp --sport 0:65535 --dport 23 -j ACCEPT'
        self.assertEquals(None, c.append(line.split(" ")))
        self.assertEquals([['[9:10]', '-A', 'INPUT', '-p', 'tcp',
                        '-m', 'tcp', '--sport', '0:65535',
                        '--dport', '23', '-j', 'ACCEPT']], c.liste)
        counters = line.split(" ")[0]
        (cnt, byt) = extract_pkt_cntr(counters)
        self.assertEquals(['9'], c.cntrs)
        self.assertEquals(['10'], c.bytes)
        self.assertEquals(1, c.make_partitions())


if __name__ == "__main__":
        unittest.main()

