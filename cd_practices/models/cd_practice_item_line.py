from odoo import fields, models


class CdPracticeItemLine(models.Model):
    """Línea de un elemento. Se usa en los ejercicios de relaciones (bloque 3)."""

    _name = 'cd.practice.item.line'
    _description = 'Línea de elemento de prácticas'

    name = fields.Char(string='Descripción', required=True)
    item_id = fields.Many2one(
        'cd.practice.item',
        string='Elemento',
        required=True,
        ondelete='cascade',
    )
    quantity = fields.Integer(string='Cantidad', default=1)
    price_unit = fields.Float(string='Precio unitario')

    # =========================================================================
    # EJERCICIO 11 · Bloque 2 · Test: TestFields.test_ex11_related_owner
    # -------------------------------------------------------------------------
    # Crea en ESTE modelo un campo owner_id (Many2one a res.partner) que sea
    # un campo related de item_id.owner_id, sin almacenar.
    # PISTA DE SINTAXIS
    #   owner_id = fields.Many2one(
    #       'res.partner',
    #       string='Propietario',
    #       related='item_id.owner_id',
    #       store=False,
    #   )
    # El test comprueba que línea.owner_id == elemento.owner_id.
    # =========================================================================
