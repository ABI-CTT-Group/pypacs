============
Installation
============

Prerequisites
=============

* Python3
* Git
* `dcmtk <https://dicom.offis.de/dcmtk.php.en>`_

  .. code-block::

     sudo apt-get install -y dcmtk

1. Clone the Pypacs repository
==============================

.. code-block:: bash

   git clone https://github.com/ABI-CTT-Group/pypacs.git

2. Install Python dependencies
==============================

It is recommended to install the dependencies using a virtual environment. See the instruction below:

#. Create a virtual environment

.. code-block::

   python3 -m venv venv/

#. Activate the virtual environment

.. code-block::

   source venv/bin/activate

#. install the dependencies

.. code-block::

   pip install -r requirements.txt


