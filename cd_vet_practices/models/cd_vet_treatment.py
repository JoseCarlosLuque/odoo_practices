from odoo import fields, models


class CdVetTreatment(models.Model):
    """Tratamiento aplicado a una mascota. Se usa en los ejercicios de relaciones (bloque 3)."""

    _name = 'cd.vet.treatment'
    _description = 'Tratamiento veterinario'

    name = fields.Char(string='Tratamiento', required=True)
    pet_id = fields.Many2one(
        'cd.vet.pet',
        string='Mascota',
        required=True,
        ondelete='cascade',
    )
    quantity = fields.Integer(string='Sesiones', default=1)
    price_unit = fields.Float(string='Precio por sesión')

    # =========================================================================
    # EJERCICIO 11 · Bloque 2 · Test: TestFields.test_ex11_related_owner
    # -------------------------------------------------------------------------
    # Crea en ESTE modelo un campo owner_id (Many2one a res.partner) que sea
    # un campo related de pet_id.owner_id, sin almacenar.
    # PISTA DE SINTAXIS
    #   owner_id = fields.Many2one(
    #       'res.partner',
    #       string='Dueño',
    #       related='pet_id.owner_id',
    #       store=False,
    #   )
    # El test comprueba que tratamiento.owner_id == mascota.owner_id.
    # =========================================================================
