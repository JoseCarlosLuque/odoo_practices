from odoo import fields, models


class ResPartner(models.Model):
    """Extensión de res.partner para los ejercicios de herencia de modelos core."""

    _inherit = 'res.partner'

    # =========================================================================
    # EJERCICIO 26 · Bloque 4 · Test: TestViews.test_ex26_partner_fields
    # -------------------------------------------------------------------------
    # Añade aquí a res.partner:
    #   1) authored_book_ids: One2many con cd.library.book (inverse author_id).
    #   2) authored_book_count: Integer computado (no hace falta store) que
    #      cuente authored_book_ids. Depende de authored_book_ids.
    #   3) action_view_authored_books(): devuelve un ir.actions.act_window
    #      (dict) que abra los libros del autor:
    #         type, name, res_model='cd.library.book', view_mode='list,form',
    #         domain=[('author_id', '=', self.id)]
    # PISTA DE SINTAXIS
    #   authored_book_ids = fields.One2many('cd.library.book', 'author_id',
    #                                       string='Libros')
    #
    #   @api.depends('authored_book_ids')
    #   def _compute_authored_book_count(self):
    #       ...
    # =========================================================================
