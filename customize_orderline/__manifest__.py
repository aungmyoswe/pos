# -*- coding: utf-8 -*-
{
    'name': 'Listview Style in POS Cart View',
    'version': '12.0.1',
	'description': 'POS order line in POS Cart.',
    'summary': 'POS order table style in POS Screen cart view.',
    'category': 'Point Of Sale',
    'author': 'Matrix',
    'sequence': 10,
    'depends': ['point_of_sale'],
    'data': [
        'views/header.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
    'price': 50,
    'license': 'OPL-1',
    'currency': 'EUR',
}
