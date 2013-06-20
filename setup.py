#!/usr/bin/env python

from distutils.core import setup

setup(name='iptables-optimizer',
    description='runtime iptables sorting by packet-counters',
    long_description="""
    iptables-optimizer
    ==================

    This little python script is run by a wrapper (shell), driven
    by cron. The wrapper needs to be run as root because it calls
    iptables-save and iptables-restore.

    Goal is to have all chains sorted by decreasing packet-counters,
    as each incoming packet is searched along the chains within one
    single core during interrupt processing. From a statistical point
    of view, the load decreases by having them sorted by the counters,
    if you have a lot of unused but neccessary commands within the
    chains. The sorting is done within the lists build from the
    iptables-save. Afterwards printed to stdout gives you a chance to
    inspect them before restoring to the kernel by iptables-restore.

    And of course, some resticitions are respected, especially no
    rules with different policies are sorted crossover.
    """,
    version='0.9.1',
    license='GNU General Public License version 3 (or later)',
    platforms='GNU/Linux 2.6.x, GNU/Linux 3.x',
    author='Johannes Hubertz',
    author_email='Johannes@hubertz.de',
    url='https://github.com/sl0/opti.git',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        'Topic :: System :: Networking :: Firewalls',
        'Topic :: Utilities',
    ],
    py_modules=['iptables_optimizer'],
    )
