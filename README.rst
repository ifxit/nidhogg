=======
nidhogg
=======

.. image:: https://travis-ci.org/ifxit/nidhogg.svg?branch=master
    :target: https://travis-ci.org/ifxit/nidhogg


Nidhogg is a wrapper interface to **Netapp filers** accross **versions and technologies** (sevenmode, vserver)
using the native Netapp REST API. It provides a consistent interface for the most common operations.


Installing nidhogg
==================

You can install ``nidhogg`` using::

    pip install nidhogg

``nidhogg`` requires Python >= 2.7 or Python >= 3.4.


Please help out
===============

This project is still under development. Feedback and suggestions are
very welcome and I encourage you to use the `Issues list <http://github.com/ifxit/nidhogg/issues>`_
on Github to provide that feedback.

Feel free to fork this repo and to commit your additions. For a list
of all contributors, please see the file `AUTHORS.txt`.

You will need `py.test` to run the tests.


License terms
=============

Nidhogg is published under the permissive terms of the MIT License, see
the file `LICENSE.txt`. Although the MIT License does not
require you to share any modifications you make to the source code,
you are very much encouraged and invited to contribute back your
modifications to the community, preferably in a Github fork, of
course.


Usage
=====

.. code-block:: python

    import nidhogg
    filer = nidhogg.get_netapp("filer99.example.com", "<username>", "<password>")
    filer.create_qtree("volume_name", "qtree_name")


Attention: The ``username`` must be allowed to access the NetApp REST API.


Documentation
=============

Look at the `API documentation <https://nidhogg.readthedocs.org>`_.


Planned further work
====================

* support snapmirror methods for Netapp vserver mode
* add EMC Isilon wrapper


Nidhogg? Is this an acronym? Or what!?
======================================

No acronym, go to http://en.wikipedia.org/wiki/Nidhogg.

If you want to use it as an acronym, use this:

**N**\ ifty **I**\ nterface **D**\ eveloped by **H**\ andsome **O**\ doriferous **G**\ entle **G**\ eeks
