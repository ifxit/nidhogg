.. Nidhogg documentation master file, created by
   sphinx-quickstart on Thu May 28 09:48:45 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Nidhogg's documentation!
===================================

.. note::

   NetApp Interface done right!


.. image:: https://travis-ci.org/ifxit/nidhogg.svg?branch=master
    :target: https://travis-ci.org/ifxit/nidhogg


Contents:


.. toctree::
   :maxdepth: 20
   :numbered: 1
   :glob:

   nidhogg_basics.rst
   nidhogg_api.rst
   nidhogg_sevenmode.rst
   nidhogg_clustermode.rst
   nidhogg_data_types.rst
   nidhogg_helpers.rst
   nidhogg_changelog.rst


Purpose
=======

This library is a wrapper interface to **Netapp filers** accross **versions and technologies** (sevenmode, vserver)
using the native Netapp REST API. It provides a consistent interface for the most common operations.


Installation
============

.. code-block:: python

    pip install nidhogg


Usage
=====

.. code-block:: python

    import nidhogg
    filer = nidhogg.get_netapp("filer99.example.com", "<username>", "<password>")
    filer.create_qtree("volume_name", "qtree_name")


Planned further work
====================

* support snapmirror methods for Netapp vserver mode
* add EMC Isilon wrapper


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
