# =============================================================================
# EJERCICIO 21 · Bloque 3 · Test: TestRelations.test_ex21_inherits_owner
# -----------------------------------------------------------------------------
# Crea en ESTE archivo el modelo cd.vet.owner usando delegación
# (_inherits) sobre res.partner. Al terminar, impórtalo en models/__init__.py
# (ya está importado, así que basta con definir la clase).
#
# El modelo debe tener:
#   _name = 'cd.vet.owner'
#   _inherits = {'res.partner': 'partner_id'}
#
#   partner_id  = Many2one('res.partner', required=True, ondelete='cascade')
#   owner_code  = Char
#   category    = Selection([('standard', 'Estándar'), ('premium', 'Premium')])
#   join_date   = Date
#
# Con _inherits, los campos de res.partner (name, email, ...) se leen y
# escriben directamente sobre el dueño y se sincronizan con el partner.
# PISTA DE SINTAXIS
#   from odoo import fields, models
#
#   class CdVetOwner(models.Model):
#       _name = 'cd.vet.owner'
#       _description = 'Dueño de mascota'
#       _inherits = {'res.partner': 'partner_id'}
#
#       partner_id = fields.Many2one('res.partner', string='Contacto',
#                                    required=True, ondelete='cascade')
#       ...
#
# El test:
#   - comprueba que existe el modelo,
#   - crea un dueño con {'name': '...', 'owner_code': '...'},
#   - verifica que se ha creado el res.partner y que name se sincroniza en
#     ambos sentidos.
# =============================================================================
