from odoo import fields, models


class ResPartner(models.Model):
    """Extensión de res.partner para los ejercicios de herencia de modelos core."""

    _inherit = 'res.partner'

    # =========================================================================
    # EJERCICIO 26 · Bloque 4 · Test: TestViews.test_ex26_partner_fields
    # -------------------------------------------------------------------------
    # Añade aquí a res.partner:
    #   1) practice_item_ids: One2many con cd.practice.item (inverse owner_id).
    #   2) practice_item_count: Integer computado (no hace falta store) que
    #      cuente practice_item_ids. Depende de practice_item_ids.
    #   3) action_view_practice_items(): devuelve un ir.actions.act_window
    #      (dict) que abra los elementos del partner:
    #         type, name, res_model='cd.practice.item', view_mode='list,form',
    #         domain=[('owner_id', '=', self.id)]
    # PISTA DE SINTAXIS
    #   practice_item_ids = fields.One2many('cd.practice.item', 'owner_id',
    #                                       string='Elementos')
    #
    #   @api.depends('practice_item_ids')
    #   def _compute_practice_item_count(self):
    #       ...
    # =========================================================================
