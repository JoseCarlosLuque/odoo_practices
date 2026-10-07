from odoo import fields, models


class CdClothesVariant(models.Model):
    """Variante de una prenda (talla, color...). Se usa en los ejercicios de relaciones (bloque 3)."""

    _name = 'cd.clothes.variant'
    _description = 'Variante de prenda'

    name = fields.Char(string='Variante', required=True)
    product_id = fields.Many2one(
        'cd.clothes.product',
        string='Prenda',
        required=True,
        ondelete='cascade',
    )
    stock = fields.Integer(string='Stock', default=1)
    price_extra = fields.Float(string='Suplemento de precio')

    # =========================================================================
    # EJERCICIO 11 · Bloque 2 · Test: TestFields.test_ex11_related_supplier
    # -------------------------------------------------------------------------
    # Crea en ESTE modelo un campo supplier_id (Many2one a res.partner) que sea
    # un campo related de product_id.supplier_id, sin almacenar.
    # PISTA DE SINTAXIS
    #   supplier_id = fields.Many2one(
    #       'res.partner',
    #       string='Proveedor',
    #       related='product_id.supplier_id',
    #       store=False,
    #   )
    # El test comprueba que variante.supplier_id == prenda.supplier_id.
    # =========================================================================
