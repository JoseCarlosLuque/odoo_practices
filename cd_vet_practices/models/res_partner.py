from odoo import fields, models


class ResPartner(models.Model):
    """Extensión de res.partner para los ejercicios de herencia de modelos core."""

    _inherit = 'res.partner'

    # =========================================================================
    # EJERCICIO 26 · Bloque 4 · Test: TestViews.test_ex26_partner_fields
    # -------------------------------------------------------------------------
    # Añade aquí a res.partner:
    #   1) pet_ids: One2many con cd.vet.pet (inverse owner_id).
    #   2) pet_count: Integer computado (no hace falta store) que cuente
    #      pet_ids. Depende de pet_ids.
    #   3) action_view_pets(): devuelve un ir.actions.act_window (dict) que
    #      abra las mascotas del dueño:
    #         type, name, res_model='cd.vet.pet', view_mode='list,form',
    #         domain=[('owner_id', '=', self.id)]
    # PISTA DE SINTAXIS
    #   pet_ids = fields.One2many('cd.vet.pet', 'owner_id', string='Mascotas')
    #
    #   @api.depends('pet_ids')
    #   def _compute_pet_count(self):
    #       ...
    # =========================================================================
