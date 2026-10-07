from odoo import fields, models


class ResPartner(models.Model):
    """Extensión de res.partner para los ejercicios de herencia de modelos core."""

    _inherit = 'res.partner'

    # =========================================================================
    # EJERCICIO 26 · Bloque 4 · Test: TestViews.test_ex26_partner_fields
    # -------------------------------------------------------------------------
    # Añade aquí a res.partner:
    #   1) product_ids: One2many con cd.clothes.product (inverse supplier_id).
    #   2) product_count: Integer computado (no hace falta store) que cuente
    #      product_ids. Depende de product_ids.
    #   3) action_view_products(): devuelve un ir.actions.act_window (dict) que
    #      abra las prendas del proveedor:
    #         type, name, res_model='cd.clothes.product', view_mode='list,form',
    #         domain=[('supplier_id', '=', self.id)]
    # PISTA DE SINTAXIS
    #   product_ids = fields.One2many('cd.clothes.product', 'supplier_id',
    #                                 string='Prendas')
    #
    #   @api.depends('product_ids')
    #   def _compute_product_count(self):
    #       ...
    # =========================================================================
