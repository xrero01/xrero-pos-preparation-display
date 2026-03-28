{
    'name': 'Xrero POS Preparation Display',
    'version': '17.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Kitchen display system for POS order preparation tracking',
    'description': """
Xrero POS Preparation Display
==============================
Kitchen Display System (KDS) for Odoo 17 Point of Sale.

Kitchen staff can view and manage POS orders in real-time across
configurable preparation stages.

**Features:**
- Configurable preparation displays per kitchen/bar station
- Multiple preparation stages (New → In Progress → Ready → Done)
- Category-based order filtering (Food, Drinks, etc.)
- Kanban board with drag-and-drop stage progression
- Order notes and timestamps
- Multi-POS shop support
    """,
    'author': 'Xrero',
    'website': 'https://www.xrero.com',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/preparation_stage_data.xml',
        'views/preparation_display_views.xml',
        'views/preparation_order_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
