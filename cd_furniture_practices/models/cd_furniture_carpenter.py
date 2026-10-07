# =============================================================================
# EJERCICIO 21 · Bloque 3 · Test: TestRelations.test_ex21_inherits_carpenter
# -----------------------------------------------------------------------------
# Crea en ESTE archivo el modelo cd.furniture.carpenter usando delegación
# (_inherits) sobre res.partner. Al terminar, impórtalo en models/__init__.py
# (ya está importado, así que basta con definir la clase).
#
# El modelo debe tener:
#   _name = 'cd.furniture.carpenter'
#   _inherits = {'res.partner': 'partner_id'}
#
#   partner_id     = Many2one('res.partner', required=True, ondelete='cascade')
#   carpenter_code = Char
#   category       = Selection([('apprentice', 'Aprendiz'), ('master', 'Maestro')])
#   join_date      = Date
#
# Con _inherits, los campos de res.partner (name, email, ...) se leen y
# escriben directamente sobre el carpintero y se sincronizan con el partner.
# PISTA DE SINTAXIS
#   from odoo import fields, models
#
#   class CdFurnitureCarpenter(models.Model):
#       _name = 'cd.furniture.carpenter'
#       _description = 'Carpintero de fábrica'
#       _inherits = {'res.partner': 'partner_id'}
#
#       partner_id = fields.Many2one('res.partner', string='Contacto',
#                                    required=True, ondelete='cascade')
#       ...
#
# El test:
#   - comprueba que existe el modelo,
#   - crea un carpintero con {'name': '...', 'carpenter_code': '...'},
#   - verifica que se ha creado el res.partner y que name se sincroniza en
#     ambos sentidos.
# =============================================================================
