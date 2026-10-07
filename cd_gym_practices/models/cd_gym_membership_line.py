from odoo import fields, models


class CdGymMembershipLine(models.Model):
    """Servicio incluido en una cuota. Se usa en los ejercicios de relaciones (bloque 3)."""

    _name = 'cd.gym.membership.line'
    _description = 'Servicio de cuota'

    name = fields.Char(string='Servicio', required=True)
    membership_id = fields.Many2one(
        'cd.gym.membership',
        string='Cuota',
        required=True,
        ondelete='cascade',
    )
    quantity = fields.Integer(string='Sesiones', default=1)
    price_unit = fields.Float(string='Precio por sesión')

    # =========================================================================
    # EJERCICIO 11 · Bloque 2 · Test: TestFields.test_ex11_related_partner
    # -------------------------------------------------------------------------
    # Crea en ESTE modelo un campo partner_id (Many2one a res.partner) que sea
    # un campo related de membership_id.partner_id, sin almacenar.
    # PISTA DE SINTAXIS
    #   partner_id = fields.Many2one(
    #       'res.partner',
    #       string='Socio',
    #       related='membership_id.partner_id',
    #       store=False,
    #   )
    # El test comprueba que servicio.partner_id == cuota.partner_id.
    # =========================================================================
