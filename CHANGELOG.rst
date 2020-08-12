==============
Change history
==============

0.5.5 (2020-08-12)
=================

* Added year-attribute to ProcessType and relevant filtering
* All existing ProcessType instances will get year 2017
* Pre-load Selectielijst 2020
* Updated Django to 2.2.15
* Updated npm libraries

0.5.4 (2019-07-08)
==================

Improved documentation

Also bumped to Django 2.2.x (LTS).

0.5.3 (2019-07-08)
==================

Updated to latest vng-api-common

* Applied ``black`` code formatting
* Set up Travis CI
* Added versioning tooling

0.5.2 (2019-04-04)
==================

Added missing dependency

0.5.1 (2019-02-27)
==================

Maturity release

* Bumped to security releases of dependencies
* Swapped out zds-schema for vng-api-common
* Improved documentation & licensing info
* Updated API spec

0.5.0 (2019-02-27)
==================

Added management command to load data from Excel

0.4.0 (2019-02-20)
==================

Add generieke-resultaattypeomschrijving to the API

0.3.0 (2019-02-08)
==================

Added ``Resultaat`` resource to the API.

Resultaat is combined with ``ProcesType`` to be able to determine an
archiving regime for particular cases with particular results.

0.2.0 (2019-01-15)
==================

Fix query for ``ProcesType``.

0.2.0 (2019-01-15)
==================

Added ``ProcesType`` resource to the API.

0.1.0
=====

* Initial release.
