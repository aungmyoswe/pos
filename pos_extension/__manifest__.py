{
    'name'          : "pos_extension",
    'version'       : "12.1.0.1",
    'category'      : "Point of sale",
    'author'        : "Yi Yi Aung",
    'email'         : "yiyiaung@asiamatrixsoftware.com",
    'website'       : "asiamatrixsoftware.com",
    'description'   : """
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    This module is to search with the Receipt Ref title
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    The POS_extension module is handle from the order of POS from DB""", 
    'depends'       : ['point_of_sale'],
    'data': ['views/pos.xml',
    ],
    'images'        : ['static/description/icon.png'],
    'auto_install'  : False,
    'installable'   : True,
    'applicaton'    : True,
}