{
    'name'              : 'expense_extension',
    'version'           : '12.0.1.1',
    'category'          : 'expense',
    'author'            : 'Yi Yi Aung',
    'email'             : 'yiyiaung@asiamatrixsoftware.com',
    'website'           : 'asiamatrixsoftware.com',
    'description'       : """
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
   This module is to change the Quantity as read only
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   
    Expense_extension is to change the Quantity type""",

    'depends'           : ['hr_expense'],
    'data'              : ['views/expense_extension_view.xml'],
    'auto_install'      : False,
    'installable'       : True,
    'applicatiion'      : True,
}