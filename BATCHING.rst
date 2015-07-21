Batch exporting
---------------

For batch exporting, there is a utility python script that will try and
reduce memory usage as much as possible by batching the exports and
restarting zope in between.

It lives in scripts/export_batched.py if you have the egg checked out.
Otherwise copy it from github into your own project:

https://github.com/netsight/collective.jsonify/blob/master/scripts/export_batched.py

Usage:
======

For a full list of options run:

.. code:: bash

	  export_batched.py -h
