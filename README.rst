
lvm scraper
==========================================

|py| |pypi| |Build Status| |docs| |Coverage Status|

``lvm scraper`` scraps data

Features
--------
- scraps data from the rabbitmq exchange
- simple web interface
- creates 8key fits cards from data

Installation
------------

``lvm scraper`` can be installed using ``pip`` as

.. code-block:: console

    pip install sdss-lvmscraper

or from source

.. code-block:: console

    git clone https://github.com/sdss/lvmscraper
    cd lvmscraper
    pip install .

Quickstart
----------

.. code-block:: console

    poetry run lvmscraper start
    
Todo
----

Usage
-----

- Start some actors
- The actor interface has two commands data & fits with an option --filter

.. code-block:: console

    #> clu
    lvm.scraper data
    10:03:03.729 lvm.scraper >
    10:03:03.751 lvm.scraper : {
       ...
    }
    lvm.scraper data --filter lvm.*.foc
    10:03:20.792 lvm.scraper >
    10:03:20.858 lvm.scraper : {
       ...
    }
    lvm.scraper fits
    10:03:27.498 lvm.scraper >
    10:03:27.507 lvm.scraper : {
       ...
    }
    lvm.scraper fits --filter *.foc
    10:03:37.945 lvm.scraper >
    10:03:37.957 lvm.scraper : {
      ...
    }


- On port 8085 there is a webserver    



.. |Build Status| image:: https://img.shields.io/github/workflow/status/sdss/lvmscraper/Test
    :alt: Build Status
    :target: https://github.com/sdss/lvmscraper/actions

.. |Coverage Status| image:: https://codecov.io/gh/sdss/lvmscraper/branch/master/graph/badge.svg?token=i5SpR0OjLe
    :alt: Coverage Status
    :target: https://codecov.io/gh/sdss/lvmscraper

.. |py| image:: https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9-blue
    :alt: Python Versions
    :target: https://docs.python.org/3/

.. |docs| image:: https://readthedocs.org/projects/docs/badge/?version=latest
    :alt: Documentation Status
    :target: https://lvmscraper.readthedocs.io/en/latest/?badge=latest

.. |pypi| image:: https://badge.fury.io/py/sdss-lvmscraper.svg
    :alt: PyPI version
    :target: https://badge.fury.io/py/sdss-lvmscraper

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
