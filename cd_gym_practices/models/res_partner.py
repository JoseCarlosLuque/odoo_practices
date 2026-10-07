from odoo import fields, models


class ResPartner(models.Model):
    """Extensión de res.partner para los ejercicios de herencia de modelos core."""

    _inherit = 'res.partner'

    # =========================================================================
    # EJERCICIO 26 · Bloque 4 · Test: TestViews.test_ex26_partner_fields
    # -------------------------------------------------------------------------
    # Añade aquí a res.partner:
    #   1) membership_ids: One2many con cd.gym.membership (inverse partner_id).
    #   2) membership_count: Integer computado (no hace falta store) que cuente
    #      membership_ids. Depende de membership_ids.
    #   3) action_view_memberships(): devuelve un ir.actions.act_window (dict)
    #      que abra las cuotas del socio:
    #         type, name, res_model='cd.gym.membership', view_mode='list,form',
    #         domain=[('partner_id', '=', self.id)]
    # PISTA DE SINTAXIS
    #   membership_ids = fields.One2many('cd.gym.membership', 'partner_id',
    #                                    string='Cuotas')
    #
    #   @api.depends('membership_ids')
    #   def _compute_membership_count(self):
    #       ...
    # =========================================================================
