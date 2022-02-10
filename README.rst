
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

    poetry run lvmscraper -vvv  start --debug



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
