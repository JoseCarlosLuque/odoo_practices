{
    'name': "cd_vet_practices",

    'summary': "Módulo de ejercicios para practicar la ORM y herramientas de Odoo 19 (clínica veterinaria)",

    'description': """
Módulo de prácticas de Odoo 19 con temática de clínica veterinaria.

Cada ejercicio está marcado en el código con un bloque de comentarios
'EJERCICIO N' y, casi siempre, con un método que lanza NotImplementedError.
Resuelve los ejercicios y valida tus soluciones ejecutando los tests:

    odoo -u cd_vet_practices --stop-after-init --test-enable --test-tags=cd_vet_practice

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
        'security/cd_vet_security.xml',
        'security/ir.model.access.csv',
        'views/cd_vet_pet_views.xml',
        'views/cd_vet_visit_views.xml',
        'views/cd_vet_tag_views.xml',
        'views/res_partner_views.xml',
        'wizards/cd_vet_visit_wizard_views.xml',
        'data/cd_vet_actions.xml',
        'data/cd_vet_cron.xml',
        'views/menus.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
