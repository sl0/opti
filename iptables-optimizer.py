#!/usr/bin/env python2.6
# -*- mode: python -*-
# -*- coding: utf-8 -*-
#
"""
    iptables-optimizer.py:
    optimize iptables commands in kernel
    in relation to usage (paket counters)

Author:     sl0.self@googlemail.com
Date:       2012-12-07
Version:    0.6
License:    GNU General Public License version 3 or later

This little helper is intended to optimize a large ruleset
in iptables paketfilter chains, optimization target is throughput.

All chains are searched for consecutive ACCEPT-rules, these
patitions in every chain are sorted on their paket-counter values.
Of course, if there are others, f.e. drop-rules or branches to
userdefined chains, these are untouched for not destroying
admistrators artwork.

The following is done for the reason of a system-crash while 
having concurring iptables-commands, which never seem to be a 
good idea.

optimizer now applies a new ruleset, if given in a file
/root/auto-apply having executable bit permission set. So the 
file may be copied onto the system, which can last some time. 
optimizer ignores it, until the permission is set to executable 
(chmod +x), which is a simple and very quick operation. After 
having run the command 'iptables-restore -c < /root/auto-apply'
the file is renamed to /root/auto-apply-old. 
Usually it might be used at next reboot-time to get the same 
state.

Comments, suggestions, improvements welcome!

Have Fun!
"""

import sys
import os
import subprocess

def execute(cmd):
    """execute cmd through subproces"""
    #print "E:", cmd
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    ret_val = proc.returncode
    if len(stderr) > 0 or ret_val > 0:
        print "got err:  ", stderr
        print "returned: ", str(ret_val)
        print "aborting"
	sys.exit(1)
    return (stdout, stderr)

def new_ruleset_present(doit=False, pathname='/root/auto-apply'):
    """look for new rulest given in file: /root/auto-apply
    if its's present _and_ executable, do corresponding 
    iptables-restore and rename it to auto-apply-old."""
    if (os.access(pathname, os.W_OK) and not os.access(pathname, os.X_OK)):
        print "news coming in, file is busy written..."
        return False
    try:
        if not doit and (os.access(pathname, os.X_OK)):
            return True
        if (os.access(pathname, os.X_OK)):
            cmd = "/sbin/iptables-restore < " + pathname
            print "Action: executing:", cmd
            execute(cmd)
            oldname = pathname + "-old"
            print "Action: renaming %s to %s\n" % (pathname, oldname)
            os.rename(pathname, oldname)
    except:
        #print "cooling"
        return False
    return False

def get_cntrs():
    """get chain content through subproces"""
    return execute('/sbin/iptables-save -c -t filter')

def reset_cntrs():
    """reset all paket and byte counters through subproces to zero"""
    return execute('/sbin/iptables -Z')

def extern_sleep(duration=3):
    """external visible process for long sleep periods"""
    dura = int(duration)
    cmd = "/bin/sleep %d" % (dura)
    s = ""
    e =""
    try:
        (s,e) = execute(cmd)
    except ValueError, err:
        print s, e, err
    return (s,e)

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
        """create a chain just from it's name"""
        self.name = name
        self.liste = []
        self.cntrs = []
        self.bytes = []
        self.partitions = []

    def append(self,line_list):
        """first save full content """
        self.liste.append(line_list)
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
        """move position upwards where it belongs to
        list_point is found in cntrs (value start with 0),
        insert_point in kernel(value starts with 1)
        """
        list_point = int(self.find_ins_point(position, part_start))
        insert_point = list_point + 1
        to_del = position + 2
        ctr = self.cntrs[position]
        element = self.cntrs.pop(position)
        self.cntrs.insert(list_point, element)
        byt = self.bytes[position]
        element = self.bytes.pop(position)
        self.bytes.insert(list_point, element)
        cmd = "-c " + ctr + " " + byt 
        for rul in self.liste[position][3:]:
            cmd = cmd + " " + rul
        execute("/sbin/iptables -I " + self.name + " " + str(insert_point) + " " + cmd)
        execute("/sbin/iptables -D " + self.name + " " + str(to_del))

    def opti(self):
        """optimze this chain due to paket counters"""
        ret_val = 0
        len_val = len(self.liste)
        if len_val < 1:
            return (len_val, ret_val)
        self.make_partitions()
        for part in self.partitions:
            start = part[0]
            last = part[1] + 1
            par_val = 0
            for act in range(start + 1, last):
                if int(self.cntrs[act]) > int(self.cntrs[act - 1]):
                    self.mov_up(act, start)
                    par_val += 1
                    ret_val += 1
                    if new_ruleset_present():
                        return(len_val, ret_val)
            ret_val += par_val
        return (len_val, ret_val)

class Filter():
    """this is a filter group, may be filter, mangle, nat, raw"""

    def __init__(self, name, count):
        print "reading tables ...", count
        self.chains = {} # keep track of my chains
        self.name = name
        (o,e) = get_cntrs()   # read kernel through shell-cmd
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
        """optimize all chains, one pass"""
        ret_val = 0;
        print "%-9s: %-15s %5s  %5s" % ("Chain", "Partitions", "Moved", "Total")
        for name in self.chains.keys():
            (length, moved) = self.chains[name].opti()
            ret_val += moved
            parts = ""
            for part in self.chains[name].partitions:
                parts += str(part) 
                print "%-9s: %-15s %5d  %5d" % (name, str(part), moved, length)
        return ret_val


if __name__ == "__main__":
    unbufd = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = unbufd
    k = 1       # global loop counter
    d = 450     # duration for long sleep periods
    t = .1       # duration for short sleep periods
    s = ""
    e = ""
    try:
        while True:
            new_ruleset_present(True)
            f = Filter("filter",k)
            r = f.opti()
            if r > 0:
                print "Round: ", k
            else:
                print "\r resetting counters"
                reset_cntrs()
                print "\r sleeping ", d, "seconds ...",
                for i in range(1, d):
                    (s, e) = extern_sleep(1)
                    if len(e) > 0:
                        print "stderr:", e
                    if new_ruleset_present():
                        break
                print
            k = k + 1
    except KeyboardInterrupt, err:
        print "\rUser stopped, execution terminated"


