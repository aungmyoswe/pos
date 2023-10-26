# -*- coding: utf-8 -*-
{
    'name': "POS Keyboard",

    'summary': "Keyboard Support for Odoo Point of Sale",

    'description': """
      POS Keyboard module provides complete keyboard support for Oddo’s POS interface.
      It is inspired by modal editing, and keybindings of VI. So one can perform all 
      the standard operations provided by the POS module, more efficiently with just a keyboard.
    """,

    'author': "Default™",
    'maintainer': "Gayan Weerakutti",

    'category': 'Point Of Sale',
    'version': '2.2.2',

    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],

    'images': ['images/main_screenshot.png'],

    'price': 20, 'currency': 'EUR',

    'auto_install': True,
    'installable': True,

    'license': 'OPL-1'
}
