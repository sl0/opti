.. iptables-optimizer documentation master file, created by
   sphinx-quickstart on Fri Aug 30 20:47:16 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to iptables-optimizer's documentation!
==============================================

.. image:: latency.png
   :width: 550px
   :align: right
   :alt: latency


what's up here?
===============

**iptables-optimizer** is a shell script to be called by the root user.

It calls some shell functions and a pyhton script to sort the 
current kernels iptables-chains in relation to the packet counters.
Just run it by cron as often as you need it. Sounds crazy?
Continue reading, please.

**iptables-optimizer** is licensed under GNU GPLv3 or any later version

Contents:

.. toctree::
   :maxdepth: 2

   iptables-optimizer
   plausible
   unittests
   sources




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

