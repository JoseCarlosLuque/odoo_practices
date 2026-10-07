# =============================================================================
# EJERCICIO 21 · Bloque 3 · Test: TestRelations.test_ex21_inherits_member
# -----------------------------------------------------------------------------
# Crea en ESTE archivo el modelo cd.gym.member usando delegación
# (_inherits) sobre res.partner. Al terminar, impórtalo en models/__init__.py
# (ya está importado, así que basta con definir la clase).
#
# El modelo debe tener:
#   _name = 'cd.gym.member'
#   _inherits = {'res.partner': 'partner_id'}
#
#   partner_id  = Many2one('res.partner', required=True, ondelete='cascade')
#   member_code = Char
#   level       = Selection([('basic', 'Básico'), ('pro', 'Profesional')])
#   join_date   = Date
#
# Con _inherits, los campos de res.partner (name, email, ...) se leen y
# escriben directamente sobre el socio y se sincronizan con el partner.
# PISTA DE SINTAXIS
#   from odoo import fields, models
#
#   class CdGymMember(models.Model):
#       _name = 'cd.gym.member'
#       _description = 'Socio de gimnasio'
#       _inherits = {'res.partner': 'partner_id'}
#
#       partner_id = fields.Many2one('res.partner', string='Contacto',
#                                    required=True, ondelete='cascade')
#       ...
#
# El test:
#   - comprueba que existe el modelo,
#   - crea un socio con {'name': '...', 'member_code': '...'},
#   - verifica que se ha creado el res.partner y que name se sincroniza en
#     ambos sentidos.
# =============================================================================
