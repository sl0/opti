#!/usr/bin/env python

#encoding:utf8

from iptables_optimizer import extract_pkt_cntr, Chain, Filter
import unittest


class Chain_Test(unittest.TestCase):
    '''some first tests for class Chain'''

    def test_01_create_a_chainobject(self):
        """Chain_Test: create a chainobject"""
        c = Chain("FIRST_CHAIN", "ACCEPT")
        self.assertEquals("FIRST_CHAIN", c.name)
        self.assertEquals("ACCEPT", c.policy)
        self.assertEquals([], c.liste)
        self.assertEquals([], c.cntrs)
        self.assertEquals([], c.bytes)
        self.assertEquals([], c.partitions)

    def test_02_make_partitions_0(self):
        """Chain_Test: make partitions from no rules"""
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        self.assertEquals(0, c.make_partitions())
        self.assertEquals([], c.partitions)

    def test_03_make_partitions_1a(self):
        """Chain_Test: make partitions from one rule a"""
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j ACCEPT'
        c.append(line.split(" "))
        self.assertEquals(1, c.make_partitions())
        self.assertEquals([[1, 1]], c.partitions)

    def test_04_make_partitions_1d(self):
        """Chain_Test: make partitions from one rule d"""
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j DROP'
        c.append(line.split(" "))
        self.assertEquals(1, c.make_partitions())
        self.assertEquals([[1, 1]], c.partitions)

    def test_05_make_partitions_1r(self):
        """Chain_Test: make partitions from one rule r"""
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j REJECT'
        c.append(line.split(" "))
        self.assertEquals(1, c.make_partitions())
        self.assertEquals([[1, 1]], c.partitions)

    def test_06_make_partitions_1l(self):
        """Chain_Test: make partitions from one rule l"""
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j LOG'
        c.append(line.split(" "))
        self.assertEquals(1, c.make_partitions())
        self.assertEquals([[1, 1]], c.partitions)

    def test_07_make_partitions_2a(self):
        """Chain_Test: make partitions from two rules aa"""
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

    def test_08_make_partitions_2ad(self):
        """Chain_Test: make partitions from two rules ad"""
        c = Chain("INPUT", "ACCEPT")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("ACCEPT", c.policy)
        # part 1: 1 - 1
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j ACCEPT'
        c.append(line.split(" "))
        # part 2: 2 - 2
        line = '[18:23] -A INPUT -i sl2 -j DROP'
        c.append(line.split(" "))
        self.assertEquals(2, c.make_partitions())
        self.assertEquals([[1, 1], [2, 2]], c.partitions)

    def test_09_make_partitions_5ada(self):
        """Chain_Test: make partitions from five rules adaaa"""
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

    def test_10_empty_opti_0(self):
        """Chain_Test: optimize an empty chainobject"""
        c = Chain("SECOND_CHAIN", "ACCEPT")
        self.assertEquals("SECOND_CHAIN", c.name)
        self.assertEquals("ACCEPT", c.policy)
        self.assertEquals([], c.liste)
        self.assertEquals([], c.cntrs)
        self.assertEquals([], c.bytes)
        self.assertEquals([], c.partitions)
        self.assertEquals((0, 0), c.opti())

    def test_11_insert_three_aaa(self):
        """Chain_Test: optimize three rules aaa"""
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

    def test_12_insert_three_aar(self):
        """Chain_Test: optimize three rules aar"""
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

    def test_14_insert_five_rules_with_logdrop(self):
        """Chain_Test: optimize five rules aalaa"""
        c = Chain("INPUT", "DROP")
        self.assertEquals("INPUT", c.name)
        self.assertEquals("DROP", c.policy)
        line = '[9:10] -A INPUT -p tcp -m tcp --dport 23 -j ACCEPT'
        c.append(line.split(" "))
        line = '[18:20] -A INPUT -i sl0 -j ACCEPT'
        c.append(line.split(" "))
        line = '[83:436] -A INPUT -j logdrop'
        c.append(line.split(" "))
        line = '[28:220] -A INPUT -i lo -j ACCEPT'
        c.append(line.split(" "))
        line = '[18:20] -A INPUT -i sl1 -j ACCEPT'
        c.append(line.split(" "))
        result = [['[9:10]', '-A', 'INPUT', '-p', 'tcp', '-m', 'tcp',
                    '--dport', '23', '-j', 'ACCEPT'],
                    ['[18:20]', '-A', 'INPUT', '-i', 'sl0', '-j', 'ACCEPT'],
                    ['[83:436]', '-A', 'INPUT', '-j', 'logdrop'],
                    ['[28:220]', '-A', 'INPUT', '-i', 'lo', '-j', 'ACCEPT'],
                    ['[18:20]', '-A', 'INPUT', '-i', 'sl1', '-j', 'ACCEPT']]
        self.assertEquals(result, c.liste)
        self.assertEquals(3, c.make_partitions())
        expect = [[1, 2], [3, 3], [4, 5]]
        #print "P:", c.partitions
        #print "W:", expect, " ... or something like that"
        self.assertEquals(expect, c.partitions)
        #self.assertTrue(False) # force textual output


class Filter_Test(unittest.TestCase):
    '''some first tests for class Filter'''

    def test_01_filter_file_NOread(self):
        """Filter_Test: non existant input-file"""
        self.assertRaises(Filter("filter", "not-exist-is-OK"))

    def test_02_filter_file_OKread(self):
        """Filter_Test: read reference-input"""
        self.assertIsInstance(Filter("filter", "reference-input"), Filter)

    def test_03_optimize_algorithm(self):
        """Filter_Test: optimize, check 30 moves and partitions"""
        f = Filter("filter", "reference-input")
        cnt, msg = f.opti()
        expect = """#chainname  : moves  partitions
#FORWARD    :     6  [1, 4][5, 5]
#INPUT      :    18  [1, 2][3, 3][4, 11][12, 12][13, 16][17, 17][18, 18][19, 20]
#IPSEC      :     0  [1, 1]
#OUTPUT     :     6  [1, 4][5, 5][6, 6]
"""
        self.assertEquals(30, cnt)
        #print msg
        self.assertEquals(expect, msg)

    def test_04_filter_output(self):
        """Filter_Test: check output for reference-input"""
        expect ="""# Generated by iptables-optimpizer.py from: reference-input
*filter
:INPUT ACCEPT [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
:IPSEC - [0:0]
[110:1234] -A INPUT -p tcp -m tcp --sport 1024:65535 --dport 21 -j ACCEPT
[9:10] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 23 -j ACCEPT
[50:2323] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 50 -j DROP
[1630:2323] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 23 -j ACCEPT
[150:2323] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 750 -j ACCEPT
[43:90] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 43 -j ACCEPT
[42:90] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 42 -j ACCEPT
[41:90] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 41 -j ACCEPT
[10:2323] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 10 -j ACCEPT
[9:10] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 23 -j ACCEPT
[1:230] -A INPUT -p tcp -m tcp --sport 1024:65535 --dport 20 -j ACCEPT
[50:2323] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 50 -j DROP
[280:2200] -A INPUT -i lo -j ACCEPT
[70:2323] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 70 -j ACCEPT
[60:2323] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 60 -j ACCEPT
[1:2323] -A INPUT -p tcp -m tcp --sport 1024:65535 --dport 23 -j ACCEPT
[380:3200] -A INPUT -j logdrop
[3:30] -A INPUT -p tcp -m tcp --sport    0:65535 --dport 24 -j DROP
[32:1260] -A INPUT -i eth3 -j ACCEPT
[3:260] -A INPUT -i eth2 -j ACCEPT
[4:123] -A FORWARD -i eth3 -o eth3 -j ACCEPT
[3:123] -A FORWARD -i eth2 -o eth2 -j ACCEPT
[2:123] -A FORWARD -i eth1 -o eth1 -j ACCEPT
[1:123] -A FORWARD -s 10.0.0.0/8 -d 192.168.216.0/24 -j ACCEPT
[1:123] -A FORWARD -j IPSEC
[200:0] -A OUTPUT -p tcp -m tcp --sport 20 --dport 1024:65535 -j ACCEPT
[50:123] -A OUTPUT -p tcp -m tcp --sport 23 --dport 1024:65535  -j ACCEPT
[20:20] -A OUTPUT -p tcp -m tcp --sport 21 --dport 1024:65535 -j ACCEPT
[10:10] -A OUTPUT -o lo -j ACCEPT
[80:123] -A OUTPUT -p tcp -m tcp --dport 25 -j REJECT
[50:123] -A OUTPUT -p tcp -m tcp --dport 25 -j ACCEPT
[11:1123] -A IPSEC -j ACCEPT
COMMIT
# Completed by iptables-optimizer.py from: reference-input
"""
        f = Filter("filter", "reference-input")
        f.opti()
        result = f.show()
        self.assertEquals(expect, result)


if __name__ == "__main__":
        unittest.main()
