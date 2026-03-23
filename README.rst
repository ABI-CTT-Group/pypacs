======
pypacs
======

A Python package for PACS interactions.

Prerequisites
=============

Before installing the Python package, ensure that you have installed the required system packages, such as DCMTK:

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install -y dcmtk

Installation
============

It is recommended to install the package and its dependencies using a virtual environment. The project uses ``pyproject.toml`` to manage building and dependencies.

.. code-block:: bash

    # create a virtual environment
    python3 -m venv .venv
    
    # activate the virtual environment
    source .venv/bin/activate
    
    # install the package (including dependencies) in editable mode
    pip install -e .

    # to optionally install testing dependencies as well:
    # pip install -e .[test]

Main functions
==============

- ``verify_connectivity``: verify DICOM node/AE connectivity. See ``examples/check_connectivity.py`` for a usage example.
- ``get_metadata``: query and retrieve metadata. See ``examples/query_and_save_metadata.py`` for a usage example.
- ``move_files``: send copies of DICOM files or download them. See ``examples/download_files.py`` for a usage example.

Usage Examples
==============

See the ``examples/`` folder for usage examples.

Make sure the PACS system you want to interact with is running before running the examples.
To start DCM4CHEE on bioeng100, see `Starting DCM4CHEE on bioeng100`_.

.. note::
   If you want to download the files from the PACS on bioeng100 to a receiver node (e.g. on a local machine), you need to add the receiver node/pacs to the node list in the PACS on bioeng100. See the header comment in ``examples/download_files.py`` for more details.

Starting DCM4CHEE on bioeng100
------------------------------

1. Connect to the UOA network/VPN.
2. Log into bioeng100: ``ssh breast@bioeng100``
3. Start DCM4CHEE: ``sh /home/breast/pacs/bin/run.sh``
4. The DCM4CHEE web interface will then be accessible via http://bioeng100.bioeng.auckland.ac.nz:8080/dcm4chee-web/
