# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Point of Sale Margin',
    'version' : '1.1',
    'summary': 'Point of Sale Margin',
    'sequence': 30,
    'description': """
		Point of Sale Margin
    """,
    'category': 'Point of Sale',    
    'depends' : ['point_of_sale'],
    'data': [        
        'views/pos_order_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,    
}
