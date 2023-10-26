{
    'name'          : "purchase_extension",
    'version'       : "12.1.0.3",
    'category'      : "Purcase",
    'author'        : "Yi Yi Aung",
    'email'         : "yiyiaung@asiamatrixsoftware.com",
    'website'       : "asiamatrixsoftware.com",
    'description'   : """
*******************************************************************
    This module is to add the product category fields
*******************************************************************
    Purchase_extension module is handle by purchase in DB""",

    'depends'       : ['purchase'],
    'data'          : ['views/purchase.xml'],
    'images'        : ['static/description/icon.png'],
    'auto_install'  : False,
    'installable'   : True,
    'application'   : True,

}