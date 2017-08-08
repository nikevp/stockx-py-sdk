stockx-py-sdk
=============

StockX Python3 API Wrapper

Notes
-----

This is an *unofficial* StockX SDK for Python3. This project is currently *not* unit tested and is likely full of bugs. It not recommended to use this SDK in production applications unless you really know what you're doing. Pull requests, issues, and requests for features are welcome. SDK documentation will come as features are finished.

This SDK does *not* (currently) support accounts registered with Facebook or Twitter.

Prerequisites
-------------

You'll need to create an account on `stock`_. Please make sure to register with an email+password (*not* Facebook or Twitter) at the moment.

Usage
-----

stockx.authenticate(email, password)
~~~~~~~~~~~~~~~~~~~

.. code:: py

    from stockxsdk import Stockx

    stockx = Stockx()

    email = 'YOUR EMAIL'
    password = 'YOUR PASSWORD'
    stockx.authenticate(email, password)




.. _stockx: https://stockx.com