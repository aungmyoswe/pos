{
    'name'          : 'product_extension',
    'version'       : '12.0.1.2',
    'category'      : 'product',
    'author'        : 'Yi Yi Aung',
    'email'         : 'yiyiaung@asiamatrixsoftware.com',
    'website'       : 'asiamatrixsoftware.com',
    'description'   : """
    *****************************************************
      This module is to separate Supplier and Class
    *****************************************************
      This module is handle from DB,""",
    'depends'       : ['product'],
    'data'          : [
        'views/product_extension.xml'],
    'images'        : ['static/description/icon.png'],
    'auto-install'  : False,
    'installable'   : True,
    'application'   : True,
} 