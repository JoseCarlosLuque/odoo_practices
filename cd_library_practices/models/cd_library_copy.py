from odoo import fields, models


class CdLibraryCopy(models.Model):
    """Ejemplar físico de un libro. Se usa en los ejercicios de relaciones (bloque 3)."""

    _name = 'cd.library.copy'
    _description = 'Ejemplar de biblioteca'

    name = fields.Char(string='Código de inventario', required=True)
    book_id = fields.Many2one(
        'cd.library.book',
        string='Libro',
        required=True,
        ondelete='cascade',
    )
    condition = fields.Selection(
        [
            ('good', 'Bueno'),
            ('worn', 'Desgastado'),
            ('damaged', 'Dañado'),
        ],
        string='Estado físico',
        default='good',
    )
    acquisition_price = fields.Float(string='Precio de adquisición')

    # =========================================================================
    # EJERCICIO 11 · Bloque 2 · Test: TestFields.test_ex11_related_author
    # -------------------------------------------------------------------------
    # Crea en ESTE modelo un campo author_id (Many2one a res.partner) que sea
    # un campo related de book_id.author_id, sin almacenar.
    # PISTA DE SINTAXIS
    #   author_id = fields.Many2one(
    #       'res.partner',
    #       string='Autor',
    #       related='book_id.author_id',
    #       store=False,
    #   )
    # El test comprueba que ejemplar.author_id == libro.author_id.
    # =========================================================================
