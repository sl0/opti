#!/usr/bin/env python

#encoding:utf8

from iptables_optimizer import extract_pkt_cntr, Chain, Filter
import unittest


class Chain_Test(unittest.TestCase):
    '''some first tests for class Chain'''

    def test_01_create_chainobject(self):
        c = Chain("FIRST_CHAIN", "ACCEPT")
        self.assertEquals("FIRST_CHAIN", c.name)
        self.assertEquals("ACCEPT", c.policy)
        self.assertEquals([], c.liste)
        self.assertEquals([], c.cntrs)
        self.assertEquals([], c.bytes)
        self.assertEquals([], c.partitions)

    def test_02_make_partitions_0(self):
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        self.assertEquals(0, c.make_partitions())
        self.assertEquals([], c.partitions)

    def test_02_make_partitions_1a(self):
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j ACCEPT'
        c.append(line.split(" "))
        self.assertEquals(1, c.make_partitions())
        self.assertEquals([[1, 1]], c.partitions)

    def test_02_make_partitions_1d(self):
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j DROP'
        c.append(line.split(" "))
        self.assertEquals(1, c.make_partitions())
        self.assertEquals([[1, 1]], c.partitions)

    def test_02_make_partitions_1r(self):
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j REJECT'
        c.append(line.split(" "))
        self.assertEquals(1, c.make_partitions())
        self.assertEquals([[1, 1]], c.partitions)

    def test_02_make_partitions_1l(self):
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j LOG'
        c.append(line.split(" "))
        self.assertEquals(1, c.make_partitions())
        self.assertEquals([[1, 1]], c.partitions)

    def test_02_make_partitions_2a(self):
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 2
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j ACCEPT'
        c.append(line.split(" "))
        line = '[18:23] -A INPUT -i sl0 -j ACCEPT'
        c.append(line.split(" "))
        self.assertEquals(1, c.make_partitions())
        self.assertEquals([[1, 2]], c.partitions)

    def test_02_make_partitions_2ad(self):
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j ACCEPT'
        c.append(line.split(" "))
        # part 2: 2 - 2
        line = '[18:23] -A INPUT -i sl2 -j DROP'
        c.append(line.split(" "))
        #c.make_partitions()
        self.assertEquals(2, c.make_partitions())
        self.assertEquals([[1, 1], [2, 2]], c.partitions)

    def test_02_make_partitions_5ada(self):
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j ACCEPT'
        self.assertEquals(None, c.append(line.split(" ")))
        # part 2: 2 - 2
        line = '[18:20] -A INPUT -i sl0 -j DROP'
        self.assertEquals(None, c.append(line.split(" ")))
        # part 3: 3 - 5
        line = '[18:20] -A INPUT -i sl1 -j ACCEPT'
        self.assertEquals(None, c.append(line.split(" ")))
        line = '[18:20] -A INPUT -i sl2 -j ACCEPT'
        self.assertEquals(None, c.append(line.split(" ")))
        line = '[28:220] -A INPUT -i lo -j ACCEPT'
        self.assertEquals(None, c.append(line.split(" ")))
        #   print "L:", c.liste
        self.assertEquals(3, c.make_partitions())
        self.assertEquals([[1, 1], [2, 2], [3, 5]], c.partitions)

    def test_03_empty_opti_0(self):
        c = Chain("FIRST_CHAIN", "ACCEPT")
        self.assertEquals("FIRST_CHAIN", c.name)
        self.assertEquals("ACCEPT", c.policy)
        self.assertEquals([], c.liste)
        self.assertEquals([], c.cntrs)
        self.assertEquals([], c.bytes)
        self.assertEquals([], c.partitions)
        self.assertEquals((0, 0), c.opti())

    def test_03_insert_three_aaa(self):
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j ACCEPT'
        c.append(line.split(" "))
        self.assertEquals([['[9:10]', '-A', 'INPUT', '-p', 'tcp',
                        '-m', 'tcp',
                        '--dport', '23', '-j', 'ACCEPT']], c.liste)
        counters = line.split(" ")[0]
        (cnt, byt) = extract_pkt_cntr(counters)
        self.assertEquals(['9'], c.cntrs)
        self.assertEquals(['10'], c.bytes)
        line = '[18:20] -A INPUT -i sl0 -j ACCEPT'
        self.assertEquals(None, c.append(line.split(" ")))
        line = '[28:220] -A INPUT -i lo -j ACCEPT'
        self.assertEquals(None, c.append(line.split(" ")))
        result = [['[9:10]', '-A', 'INPUT', '-p', 'tcp', '-m', 'tcp',
                    '--dport', '23', '-j', 'ACCEPT'],
                ['[18:20]', '-A', 'INPUT', '-i', 'sl0', '-j', 'ACCEPT'],
                ['[28:220]', '-A', 'INPUT', '-i', 'lo', '-j', 'ACCEPT']]
        self.assertEquals(result, c.liste)
        self.assertEquals(1, c.make_partitions())
        self.assertEquals([[1, 3]], c.partitions)
        self.assertEquals((3, 4), c.opti())

    def test_03_insert_three_aar(self):
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j ACCEPT'
        c.append(line.split(" "))
        self.assertEquals([['[9:10]', '-A', 'INPUT', '-p', 'tcp',
                        '-m', 'tcp',
                        '--dport', '23', '-j', 'ACCEPT']], c.liste)
        counters = line.split(" ")[0]
        (cnt, byt) = extract_pkt_cntr(counters)
        self.assertEquals(['9'], c.cntrs)
        self.assertEquals(['10'], c.bytes)
        line = '[18:20] -A INPUT -i sl0 -j ACCEPT'
        self.assertEquals(None, c.append(line.split(" ")))
        line = '[28:220] -A INPUT -i lo -j REJECT'
        self.assertEquals(None, c.append(line.split(" ")))
        result = [['[9:10]', '-A', 'INPUT', '-p', 'tcp', '-m', 'tcp',
                    '--dport', '23', '-j', 'ACCEPT'],
                ['[18:20]', '-A', 'INPUT', '-i', 'sl0', '-j', 'ACCEPT'],
                ['[28:220]', '-A', 'INPUT', '-i', 'lo', '-j', 'REJECT']]
        self.assertEquals(result, c.liste)
        self.assertEquals(2, c.make_partitions())
        self.assertEquals([[1, 2], [3, 3]], c.partitions)
        self.assertEquals((3, 2), c.opti())


class Filter_Test(unittest.TestCase):
    '''some first tests for class Filter'''

    def test_04_filter_file_NOread(self):
        self.assertRaises(Filter("filter", "not-exist-is-OK"))

    def test_05_filter_file_OKread(self):
        self.assertIsInstance(Filter("filter", "reference-input"), Filter)

    def test_06_optimize_algorithm(self):
        f = Filter("filter", "reference-input")
        self.assertEquals(30, f.opti())

    def test_07_filter_output(self):
        f = Filter("filter", "reference-input")
        f.opti()
        self.assertEquals(None, f.show())


if __name__ == "__main__":
        unittest.main()
