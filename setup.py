#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='iptables-optimizer',
    description='runtime iptables sorting by packet-counters',
    long_description=open('README.txt').read(),
    version='0.9.7',
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
    scripts=['iptables-optimizer'],
    )
