#!/usr/bin/env python
# -*- mode: python -*-
# -*- coding: utf-8 -*-
#
"""
    iptables-optimizer.py:
    optimize iptables ruleset in userland
    in relation to usage (paket counters)

Author:     Johannes Hubertz johannes@hubertz.de
Date:       2013-08-12
Version:    0.9.8
License:    GNU General Public License version 3 or later

This little helper is intended to optimize a large ruleset
in iptables paketfilter chains, optimization target is throughput.

All chains are partitioned now, sorting is done inside the
partitions. Sequence of partitions is never changed, these keep
untouched for not destroying admistrators artwork.

You will need a wrapper script, use optimizer.sh as example.

Comments, suggestions, improvements welcome!

Have Fun!
"""

import sys
import os


def extract_pkt_cntr(cntrs):
    """given is a string: '[pkt_cntr:byt_cntr]', we need
    pkt_cntr and byt_cntr as set of return value for comparison"""
    br1 = cntrs.replace("[", "")
    br2 = br1.replace("]", "").strip()
    pkts, byts = br2.split(':')
    return (pkts, byts)


class Chain():
    """this is representation of one chain"""

    def __init__(self, name, policy):
        """create a chain just from it's name"""
        self.name = name
        self.policy = policy
        self.liste = []
        self.cntrs = []
        self.bytes = []
        self.partitions = []

    def append(self, line_list):
        """first fill in some content, line by line"""
        self.liste.append(line_list)
        cntrs = line_list[0]
        (cnt, byt) = extract_pkt_cntr(cntrs)
        self.cntrs.append(cnt)
        self.bytes.append(byt)

    def make_partitions(self):
        """make_partitions creates a list of 2-Elements-lists,
        each representing a consecutive sequence with ACCEPT,
        DROP, or the like. One 2-Element-list is called a
        partition, it is [p_strt, p_ende], and taken form self.liste
        Numbers in partions are Element-Positions, not indices!
        It returns len(self.partitions), used for testing purpose.
        """
        self.partitions = []              # start with empty list
        number = 0
        p_policy = "DROP"
        p_po_old = None
        p_strt = 1
        p_ende = 1
        last = len(self.liste)
        for index in range(0, last):      # iterate complete list
            rule_txt = ""
            for k in self.liste[index]:
                rule_txt = rule_txt + k + " "
            if "ACCEPT" in rule_txt:
                p_policy = "ACCEPT"
            elif "DROP" in rule_txt:
                p_policy = "DROP"
            elif "REJECT" in rule_txt:
                p_policy = "REJECT"     # we have mercy with LOG or the like
            else:                       # tribute to other targets
                number += 1
                p_policy = "undef%05d" % (number)
            if p_po_old is None:        # initialize old value once
                p_po_old = p_policy
            if (p_policy == p_po_old):
                p_ende = index + 1
            else:
                self.partitions.append([p_strt, p_ende])
                p_strt = index + 1
            p_ende = index + 1
            p_po_old = p_policy
        # special case: no rules in chain
        if len(self.liste) == 0:
            self.partitions = []
        elif len(self.liste) == 1:
            self.partitions = [[1, 1]]
        else:
            self.partitions.append([p_strt, p_ende])
        retval = len(self.partitions)
        return retval

    def find_ins_point(self, act, part_start):
        """find out, where to insert rule due to pkt-cntrs"""
        val = int(self.cntrs[act])
        for run in range(part_start, act):
            if int(self.cntrs[run]) < val:
                return run
        #raise "unforeseen error condition"
        #return 0

    def mov_up(self, position, part_start):
        """move position upwards where it belongs to
        list_point is found in cntrs (value start with 0),
        insert_point in kernel(value starts with 1)
        """
        list_point = int(self.find_ins_point(position, part_start))
        tmp_rule = self.liste.pop(position)
        self.liste.insert(list_point, tmp_rule)
        paket_cnt = self.cntrs.pop(position)
        self.cntrs.insert(list_point, paket_cnt)
        bytes_cnt = self.bytes.pop(position)
        self.bytes.insert(list_point, bytes_cnt)

    def opti(self):
        """optimze this chain due to paket counters"""
        ret_val = 0
        len_val = len(self.liste)
        if len_val < 1:
            return (len_val, ret_val)
        self.make_partitions()
        for part in self.partitions:
            start = part[0] - 1
            last = part[1]
            par_val = 0
            for act in range(start + 1, last):
                if int(self.cntrs[act]) > int(self.cntrs[act - 1]):
                    self.mov_up(act, start)
                    par_val += 1
                    ret_val += 1
            ret_val += par_val
        return (len_val, ret_val)


class Filter():
    """this is a filter group, may be filter, mangle, nat, raw,
    optimzer looks on filter group only!
    """

    def __init__(self, groupname="filter", filename="reference-input"):
        """create a Filter object representing a filtergroup of iptables"""
        self.chains = {}  # keep track of my chains
        self.groupname = groupname
        self.filename = filename
        try:
            pfile = open(filename, 'r')
            for line in pfile:  # .split("\n"):
                line.replace(r"\n", " ")
                if line.startswith(":"):    # first they are defined
                    (c_name, policy, rest) = line.replace(":", "").split(" ")
                    self.chains[c_name] = Chain(c_name, policy)
                else:
                    # find chain_name from line, don't rely on position in file
                    items = line.split(" ")
                    for act in range(0, len(items)):
                        if items[act] == '-A':
                            c_name = items[act + 1]
                            #c_rest = items[act + 2:]
                            self.chains[c_name].append(items)
        except IOError as err:
            print(filename + ": ", err.strerror)

    def opti(self):
        """optimize all chains, one pass, and ready
        return sum of moved counts and partitions list for debugging
        """
        ret_val = 0
        omsg = "#chainname  : moves  partitions\n"
        for name in self.chains.keys():
            (length, moved) = self.chains[name].opti()
            ret_val += moved
            parts = ""
            for part in self.chains[name].partitions:
                parts += str(part)
            omsg += "#%-11s: %5d  %s\n" % (name, moved, parts)
        return (ret_val, omsg)

    def sequence(self):
        """keep track of all chainnames, predefined first with policy"""
        predefs = ['INPUT', 'FORWARD', 'OUTPUT']
        head_list = []
        cont_list = []
        for nam in predefs:
            cont_list.append(nam)
            line = ":%s %s [0:0]" % (nam, self.chains[nam].policy)
            head_list.append(line)
        for nam in self.chains:
            if self.chains[nam].name not in predefs:
                cont_list.append(nam)
                line = ":%s - [0:0]" % (nam)
                head_list.append(line)
        return (head_list, cont_list)

    def show(self):
        """after sorting rules, print them out"""
        out = "# Generated by iptables-optimpizer.py from: "
        out += self.filename + '\n'
        out += "*%s\n" % (self.groupname)
        head, cont = self.sequence()
        for name in head:
            out += "%s\n" % (name)
        for name in cont:
            for this in self.chains[name].liste:
                line = ""
                for items in this:
                    line += "%s " % (str(items))
                out += line.strip()
                out += "\n"
        out += "COMMIT\n"
        out += "# Completed by iptables-optimizer.py from: %s\n" % \
               (self.filename)
        return out


if __name__ == "__main__":
    try:
        f = Filter()
        result, msg = f.opti()
        sys.stderr.write(msg)  # print partition-table to stderr
        outmsg = f.show()
        print(outmsg),
    except KeyboardInterrupt as err:
        print("\rUser stopped, execution terminated")
