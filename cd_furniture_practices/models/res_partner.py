from odoo import fields, models


class ResPartner(models.Model):
    """Extensión de res.partner para los ejercicios de herencia de modelos core."""

    _inherit = 'res.partner'

    # =========================================================================
    # EJERCICIO 26 · Bloque 4 · Test: TestViews.test_ex26_partner_fields
    # -------------------------------------------------------------------------
    # Añade aquí a res.partner:
    #   1) designed_product_ids: One2many con cd.furniture.product
    #      (inverse designer_id).
    #   2) designed_product_count: Integer computado (no hace falta store) que
    #      cuente designed_product_ids. Depende de designed_product_ids.
    #   3) action_view_designed_products(): devuelve un ir.actions.act_window
    #      (dict) que abra los muebles del diseñador:
    #         type, name, res_model='cd.furniture.product', view_mode='list,form',
    #         domain=[('designer_id', '=', self.id)]
    # PISTA DE SINTAXIS
    #   designed_product_ids = fields.One2many(
    #       'cd.furniture.product', 'designer_id', string='Muebles')
    #
    #   @api.depends('designed_product_ids')
    #   def _compute_designed_product_count(self):
    #       ...
    # =========================================================================
