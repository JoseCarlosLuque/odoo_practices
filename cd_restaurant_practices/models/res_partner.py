from odoo import fields, models


class ResPartner(models.Model):
    """Extensión de res.partner para los ejercicios de herencia de modelos core."""

    _inherit = 'res.partner'

    # =========================================================================
    # EJERCICIO 26 · Bloque 4 · Test: TestViews.test_ex26_partner_fields
    # -------------------------------------------------------------------------
    # Añade aquí a res.partner:
    #   1) dish_ids: One2many con cd.restaurant.dish (inverse chef_id).
    #   2) dish_count: Integer computado (no hace falta store) que cuente
    #      dish_ids. Depende de dish_ids.
    #   3) action_view_dishes(): devuelve un ir.actions.act_window (dict) que
    #      abra los platos del chef:
    #         type, name, res_model='cd.restaurant.dish', view_mode='list,form',
    #         domain=[('chef_id', '=', self.id)]
    # PISTA DE SINTAXIS
    #   dish_ids = fields.One2many('cd.restaurant.dish', 'chef_id',
    #                              string='Platos')
    #
    #   @api.depends('dish_ids')
    #   def _compute_dish_count(self):
    #       ...
    # =========================================================================
