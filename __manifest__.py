# -*- coding: utf-8 -*-
{
    'name': "odoo_basico",

    'summary': """
        proxecto inicial
        
        """,

    'description': """
        proxecto inicial bla bla bla
    """,

    'author': "eu",
    'website': "https://www.edu.xunta.gal/centros/iesteis/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [

        'reports/report_header.xml',
        'reports/report_informacion.xml'
        'views/pedido.xml',
        'views/lineapedido.xml',
        'views/informacion.xml',
        'views/suceso.xml',
        'views/templates.xml',
        'views/menu.xml',
        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
