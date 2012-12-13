#!/usr/bin/env python

from distutils.core import setup

setup(name='iptables-optimizer',
    description='runtime iptables sorting by packet-counters',
    long_description="""
    iptables-optimizer
    ==================

    This little python script must be run as root, because it 
    spawns a lot of iptables-commands using the python-builtin 
    subprocess.

    Goal is to have all chains sorted by decreasing packet-counters,
    as each incoming packet is searched along the chains within one
    single core during interrupt processing. From a statistical point
    of view, the load decreases by having them sorted by the counters,
    if you have a lot of unused but neccessary commands within the
    chains. The sorting is done by copying a rule to a more prominent
    place within the same chain, some resticitions are respected.
    After successful copy the rule in it original place is deleted.

    Every sort-run through the chains, where nothing was changed,
    two things are done: 
        1st) the packet counters are all reset to zero.
        2nd) a file is looked up: /root/auto-apply
    It is looked up for read/write and executable access-rights, 
    both must be set. If not, nothing is done. If set, some simple
    assumptions are done: It has iptables-save format, and it sure 
    expresses the administrators intention. So then go along, the
    following command drives it into the kernel: 
        iptables-restore /root/auto-apply
    If it is not present, nothing but sleeping is done, then again 
    the sorting is done. Short duration heavy traffic will change 
    the chains not for a long period, but in short term meaning is 
    preferred over other traffic..
    """,
    version='0.7',
    license='GNU General Public License version 3 (or later)',
    platforms='GNU/Linux 2.6.x, GNU/Linux 3.x',
    author='sl0',
    author_email='sl0.self@googlemail.com',
    url='https://github.com/sl0/opti.git',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Topic :: Security',
        'Topic :: System :: Networking :: Firewalls',
        'Topic :: Utilities',
    ],
    py_modules=['iptables-optimizer'],
    )

