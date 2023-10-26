# -*- coding: utf-8 -*-
{
    'name'          : "Users Access Right",
    'author'        : "Aung Myo Swe",
    'website'       : "www.asiamatrixsoftware.com",
    'category'      : 'base',
    'summary'       : """User Access Right For Account Finance""",
    'version'       : '12.0.1.0',
    
    'description'   : """
        This Module Add user access right for Finance User that is same Advisor.
    """,
    'depends'       : ['base','stock_account'],
    'data'          : ['views/product_cost_view.xml',
        'security/access_right_view.xml',],
    'images'        : ['static/description/icon.png'],
}