

# confdb

.. contents:: On this page
    :local:
    :backlinks: none
    :depth: 1
    :class: singlecol

Name
----
`noc confdb` - ConfDB manipulation tool

Synopsis
--------

    noc confdb syntax [path ...]
               tokenizer [--object=<id>|--profile=<profile> --config=<path>]
               normalizer [--object=<id>|--profile=<profile> --config=<path>]

Description
-----------
ConfDB investigation tool

Examples
--------

Dump ConfDB syntax:

.. code-block:: text

    ./noc confdb syntax

Dump part of ConfDB syntax:

.. code-block:: text

    ./noc confdb syntax intefaces x

Dump result of object's [tokenizer](../../dev/confdb/tokenizer.md).
Managed Object ID is 120:

.. code-block:: text

    ./noc confdb tokenizer --object=120

Dump result of object's [tokenizer](../../dev/confdb/tokenizer.md),
applied to arbitrary file:

.. code-block:: text

    ./noc confdb tokenizer --object=120 --config=config.txt

Dump result of profile's [tokenizer](../../dev/confdb/tokenizer.md),
applied to arbitrary file:

.. code-block:: text

    ./noc confdb tokenizer --profile=Cisco.IOS --config=config.txt

Dump result of object's [normalizer](../../dev/confdb/normalizer.md).
Managed Object ID is 120:

.. code-block:: text

    ./noc confdb normalizer --object=120

Dump result of object's [normalizer](../../dev/confdb/normalizer.md),
applied to arbitrary file:

.. code-block:: text

    ./noc confdb normalizer --object=120 --config=config.txt

Dump result of profile's [normalizer](../../dev/confdb/normalizer.md),
applied to arbitrary file:

.. code-block:: text

    ./noc confdb normalizer --profile=Cisco.IOS --config=config.txt

See also
--------
* [ConfDB Syntax Reference](../../dev/confdb/overview.md)
* [ConfDB Normalizers](../../dev/confdb/normalizer.md)
* [ConfDB Tokenizers](../../dev/confdb/tokenizer.md)
