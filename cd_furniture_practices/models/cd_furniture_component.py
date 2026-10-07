from odoo import fields, models


class CdFurnitureComponent(models.Model):
    """Pieza de un mueble. Se usa en los ejercicios de relaciones (bloque 3)."""

    _name = 'cd.furniture.component'
    _description = 'Componente de mueble'

    name = fields.Char(string='Pieza', required=True)
    product_id = fields.Many2one(
        'cd.furniture.product',
        string='Mueble',
        required=True,
        ondelete='cascade',
    )
    quantity = fields.Integer(string='Unidades', default=1)
    price_unit = fields.Float(string='Coste unitario')

    # =========================================================================
    # EJERCICIO 11 · Bloque 2 · Test: TestFields.test_ex11_related_designer
    # -------------------------------------------------------------------------
    # Crea en ESTE modelo un campo designer_id (Many2one a res.partner) que
    # sea un campo related de product_id.designer_id, sin almacenar.
    # PISTA DE SINTAXIS
    #   designer_id = fields.Many2one(
    #       'res.partner',
    #       string='Diseñador',
    #       related='product_id.designer_id',
    #       store=False,
    #   )
    # El test comprueba que componente.designer_id == mueble.designer_id.
    # =========================================================================
