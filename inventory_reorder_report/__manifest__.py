{
    'name': 'Stock Reordering Report',
    'version': '12.0.1.2',
    'category': 'stock',
    'summary': 'Stock Reordering that shows On Hand Qty, Min Qty, Max Qty and Over/Reduce Qty.',
    'description': """
On Hand Qty, Min Qty, Max Qty and Over/Reduce Qty.
""",
    'depends': ['stock'],
    'data': [
        'wizard/inventory_wizard.xml',
        'inventory_report.xml',
        'views/inventory_report_by_warehouse.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['images/icon.png'],
}