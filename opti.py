#!/usr/bin/env python
# -*- mode: python -*-
# -*- coding: utf-8 -*-
#
"""
opti.py: optimize iptables commands in kernel
        in relation to usage (paket counters)

Author:     sl0.self@googlemail.com
Date:       2012-11-09
Version:    0.2
License:    GNU General Public License version 3 or later

This little helper is intended to optimize a large ruleset
in iptables paketfilter chains, optimization target is troughput.

All chains are searched for consecutive ACCEPT-rules, these
patitions in every chain are sorted on their paket-counter values.
Of course, if there are others, f.e. drop-rules or branches to
userdefined chains, these are untouched for not destroying
admistrators artwork.

Comments, suggestions, improvements welcome!

Have Fun!
"""

from UserDict import UserDict
import sys
import os
import subprocess
import time

def execute(cmd):
    """execute cmd through subproces"""
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    return (stdout, stderr)

def get_cntrs():
    """get chain content through subproces"""
    return execute('/sbin/iptables-save -c -t filter')

def extract_pkt_cntr(cntrs):
    """given is a string: '[pkt_cntr:byt_cntr]'
    we need pkt_cntr as return value for comparison"""
    br1 = cntrs.replace("[","")
    br2 = br1.replace("]","").strip()
    pkts, bytes = br2.split(':')
    return (pkts, bytes)

class Chain():
    """this is representation of one chain"""

    def __init__(self, name):
        self.name = name
        self.liste = []
        self.cntrs = []
        self.bytes = []
        self.partitions = []
        self.line_no = -1
        #print "# Chain created: ", name

    def append(self,line_list):
        """first save full content """
        self.liste.append(line_list)
        self.line_no += 1
        cntrs = line_list[0]
        (cnt, byt) = extract_pkt_cntr(cntrs)
        self.cntrs.append(cnt)
        self.bytes.append(byt)

    def make_partitions(self):
        """preset self.partition within self.liste
        partition means consecutive sequence with ACCEPT,
        partition is [index_start, index_ende] in self.liste
        returns len(self.partitions), unused for now
        """
        partitions = []                          # start with empty list
        index_start = -1                         # -1: not within a partition
        index__ende = -1                         # -1: not within a partition
        for i in range(0, len(self.liste)):      # iterate complete list
            if "ACCEPT" in self.liste[i]:
                if index_start == -1:
                    index_start = i
            else:
                if index_start <> -1:
                    index__ende = i - 1
            if index_start <> -1 and index__ende <> -1:
                partition = [index_start, index__ende]
                self.partitions.append(partition)
                index_start = -1
                index__ende = -1
        if index_start <> -1 and index__ende == -1:
            index__ende = len(self.liste) - 1
            partition = [index_start, index__ende]
            self.partitions.append(partition)
        retVal = len(self.partitions)
        return retVal

    def print_partitions(self):
        """show our partitions"""
        print "# %-8s: partitions: %d" % (self.name, len(self.partitions)),
        for part in self.partitions:
            print part,
        print


    def find_ins_point(self, act, part_start):
        """ find out, where to insert rule due to pkt-cntrs"""
        ret_val = 0
        val = int(self.cntrs[act])
        for run in range(part_start, act):
            if int(self.cntrs[run]) < val:
                #print "# ", self.name, "ins_point val:", val, "run:", run, int(self.cntrs[run])
                return run
        return ret_val

    def mov_up(self, position, part_start):
        """move position upwards where it belongs to"""
        point = 1 + int(self.find_ins_point(position, part_start))
        to_del = position + 2
        ctr = self.cntrs[position]
        element = self.cntrs.pop(position)
        self.cntrs.insert(point, element)
        byt = self.bytes[position]
        cmd = "-c " + ctr + " " + byt 
        for rul in self.liste[position][3:]:
            cmd = cmd + " " + rul
        execute("/sbin/iptables -I " + self.name + " " + str(point) + " " + cmd)
        execute("/sbin/iptables -D " + self.name + " " + str(to_del))


    def opti(self):
        """optimze this chain due to paket counters"""
        ret_val = 0
        if len(self.liste) < 1:
            print "# %-8s: %5d entries, nothing to do" % (self.name, len(self.liste))
            return ret_val
        self.make_partitions()
        self.print_partitions()
        for part in self.partitions:
            start = part[0]
            last = part[1] + 1
            par_val = 0
            for act in range(start + 1, last):
                if int(self.cntrs[act]) > int(self.cntrs[act - 1]):
                    self.mov_up(act, start)
                    par_val += 1
                    ret_val += 1
            print "# %-8s: %5d entries, range: %5d - %-5d, mov_up: %5d" % \
                       (self.name, len(self.liste), start, last - 1, par_val)
            ret_val += par_val
        return ret_val

class Filter():
    """this is a filter group, may be filter, mangle, nat, raw"""

    def __init__(self, name, count):
        print "reading tables ...", count
        self.chains = {} # keep track of my chains
        self.name = name
        (o,e) = get_cntrs()   # read kernel through shell-cmd
        line_no = -1 
        for line in o.split("\n"):
            if line.startswith(":"):    # first they are defined with policy and counters
                (c_name, policy, rest) = line.replace(":", "").split(" ")
                self.chains[c_name] = Chain(c_name)
            else:
                # find chain_name from line, don't rely on position or changes in file
                items = line.split(" ")
                for act in range (0, len(items)):
                    if items[act] == '-A':
                        c_name = items[act + 1]
                        c_rest = items[act + 2:]
                        self.chains[c_name].append(items)

    def opti(self):
        """ optimize all chains, one pass """
        ret_val = 0;
        for name in self.chains.keys():
            ret_val += self.chains[name].opti()
        return ret_val


if __name__ == "__main__":
    unbufd = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = unbufd
    k = 1
    s = 300
    t = 0
    lc = 0
    try:
        while True:
            f = Filter("filter",k)
            k = k + 1
            r = f.opti()
            if r > 0:
		lc += 1
                print "\rlooping", lc,
                time.sleep(2)
                #print "\r       "
            else:
                t = s
                lc = 0
                while t > 0:
                    print "\r sleeping ", t, " ",
                    time.sleep(1)
                    t = t - 1
                print
    except KeyboardInterrupt, err:
        print "\rUser stopped, excution terminated"


