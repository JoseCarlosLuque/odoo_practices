{
    'name': "cd_library_practices",

    'summary': "Módulo de ejercicios para practicar la ORM y herramientas de Odoo 19 (biblioteca)",

    'description': """
Módulo de prácticas de Odoo 19 con temática de biblioteca.

Cada ejercicio está marcado en el código con un bloque de comentarios
'EJERCICIO N' y, casi siempre, con un método que lanza NotImplementedError.
Resuelve los ejercicios y valida tus soluciones ejecutando los tests:

    odoo -u cd_library_practices --stop-after-init --test-enable --test-tags=cd_library_practice

Revisa el README.md para ver el índice completo de ejercicios y los comandos.
    """,

    'author': "José Carlos Luque Castro",
    'website': "https://github.com/JoseCarlosLuque",

    'category': 'Practices',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/cd_library_security.xml',
        'security/ir.model.access.csv',
        'views/cd_library_book_views.xml',
        'views/cd_library_loan_views.xml',
        'views/cd_library_genre_views.xml',
        'views/res_partner_views.xml',
        'wizards/cd_library_loan_wizard_views.xml',
        'data/cd_library_actions.xml',
        'data/cd_library_cron.xml',
        'views/menus.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
