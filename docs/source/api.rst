======================
API and usage examples
======================

.. automodule:: pypacs

You can find the example scripts from the *examples/* folder.

Make sure the PACS system you want to interact with is running before moving forward.

Check connectivity
------------------

Check your access to a PACS. If failed, check if the status of your PACS.

.. automethod:: pypacs::verify_connectivity

.. note::

   Usage example: see ``examples/check_connectivity.py``.

Query and save metadata
-----------------------

.. automethod:: pypacs::get_metadata

.. automethod:: pypacs::create_custom_report

.. automethod:: pypacs::save_metadata

.. note::

   Usage example:

   The example script ``examples/query_and_save_metadata.py`` shows you how to query by most of the dicom tags. The metadata will be saved in ``<pypacs>/examples/out/metadata.json``
   Please search for the variable ``query_settings`` and change it to make your owm query.

   The example script ``examples/query_and_save_metadata_advanced.py`` shows how to make advanced queries such as ``NumberOfSeriesRelatedInstances > 100``
   In this script, please update the variables ``query_settings`` for normal query conditions and ``extra_query`` for the advanced options.

Download files
--------------

.. automethod:: pypacs::move_files

.. note::

   Usage example:

   With ``download_files.py``, you can download the images to a dicom node (a folder).
   Please update the ``query_settings`` variable.
   This is a dictionary variable and you need to provide values for the keys ``StudyInstanceUID`` and ``SeriesInstanceUID``.

You can download the images to the mounted eResearch drive on either eResearch VM or on your local machine.


