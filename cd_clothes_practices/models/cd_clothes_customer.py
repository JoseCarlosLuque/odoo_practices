# =============================================================================
# EJERCICIO 21 · Bloque 3 · Test: TestRelations.test_ex21_inherits_customer
# -----------------------------------------------------------------------------
# Crea en ESTE archivo el modelo cd.clothes.customer usando delegación
# (_inherits) sobre res.partner. Al terminar, impórtalo en models/__init__.py
# (ya está importado, así que basta con definir la clase).
#
# El modelo debe tener:
#   _name = 'cd.clothes.customer'
#   _inherits = {'res.partner': 'partner_id'}
#
#   partner_id    = Many2one('res.partner', required=True, ondelete='cascade')
#   customer_code = Char
#   segment       = Selection([('regular', 'Regular'), ('vip', 'VIP')])
#   join_date     = Date
#
# Con _inherits, los campos de res.partner (name, email, ...) se leen y
# escriben directamente sobre el cliente y se sincronizan con el partner.
# PISTA DE SINTAXIS
#   from odoo import fields, models
#
#   class CdClothesCustomer(models.Model):
#       _name = 'cd.clothes.customer'
#       _description = 'Cliente de tienda'
#       _inherits = {'res.partner': 'partner_id'}
#
#       partner_id = fields.Many2one('res.partner', string='Contacto',
#                                    required=True, ondelete='cascade')
#       ...
#
# El test:
#   - comprueba que existe el modelo,
#   - crea un cliente con {'name': '...', 'customer_code': '...'},
#   - verifica que se ha creado el res.partner y que name se sincroniza en
#     ambos sentidos.
# =============================================================================
