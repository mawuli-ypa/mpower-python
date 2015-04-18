.. image:: https://api.travis-ci.org/mawuli/mpower-python.png

MPower Python Client Library
============================

This is a Python library for accessing the MPower Payments HTTP API.

Installation
------------

.. code-block:: bash

    $ sudo pip install mpower
    $ OR git clone https://github.com/mawuli/mpower-python
    $ cd mpower-python; python setup.py install`
    $ nosetests tests/  # run unit tests

Usage
-----

.. code-block:: python

    import mpower

    # runtime configs
    MP_ACCESS_TOKENS = {
        'MP-Master-Key': "Your MPower master key",
        'MP-Private-Key': "Your MPower private key",
        'MP-Token': "Your MPower token"
    }
    # defaults to False
    mpower.debug = True
    # set the access/api keys
    mpower.api_keys = MP_ACCESS_TOKENS

    # Invoice
    store = mpower.Store(name='FooBar Shop')
    items = [
        {
            "name": "VIP Ticket",
            "quantity": 2,
            "unit_price": "35.0",
            "total_price": "70.0",
            "description": "VIP Tickets for the MPower Event"
        },
    ]
    invoice = mpower.Invoice(store)
    invoice.add_items(items * 10)
    # taxes are (key,value) pairs
    invoice.add_taxes([("NHIS TAX", 23.8), ("VAT", 5)])
    invoice.add_custom_data([
        ("phone_brand", "Motorola V3"),
        ("model", "65456AH23"),
    ])

    # you can also pass the items, taxes, custom to the `create` method
    successful, response = invoice.create()
    if successful:
        do_something_with_resp(response)

    # confirm invoice
    invoice.confirm(response['token'])


    # OPR
    opr_data = {
        'account_alias': '02XXXXXXXX',
        'description': 'Hello World',
        'total_amount': 345
    }
    store = mpower.Store(name='FooBar Shop')
    opr = mpower.OPR(opr_data, store)
    # You can also pass the data to the `create` function
    successful, response = opr.create()
    if successful:
       do_something_with_response(response)
    status, _ = opr.charge({
        'token': token,
        'confirm_token': user_submitted_token
    })


    # Direct card
    card_info = {
        "card_name" : "Alfred Robert Rowe",
        "card_number" : "4242424242424242",
        "card_cvc" : "123",
        "exp_month" : "06",
        "exp_year" : "2010",
        "amount" : "300"
    }
    direct_card = mpower.DirectCard(card_info)
    # this request should fail since the card_info data is invalid
    successful, response = direct_card.process()


    # Direct Pay
    account_alias =  "02XXXXXXXX"
    amount =  30.50
    # toggle debug switch to True
    direct_pay = mpower.DirectPay(account_alias, amount)
    status, response = direct_pay.process()


License
-------
see LICENSE.txt


Contributing
------------
Issues, forks, and pull requests are welcome!


Note
----
- Some of the API calls require formal approval from MPower Payments
- For more information, please read the  `MPower Payments HTTP API`_
- Tested on Python 2.6, 2.7, and 3+. `Build Status`_

.. _MPower Payments HTTP API: http://mpowerpayments.com/developers/docs/http.html
.. _Build Status: https://api.travis-ci.org/mawuli/mpower-python.png

Authors
--------
Mawuli Adzaku <mawuli at mawuli dot me>
