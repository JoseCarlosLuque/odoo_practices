from odoo import fields, models


class CdLibraryGenre(models.Model):
    """Género literario de laboratorio.

    No tiene ejercicios propios: es el comodín para practicar relaciones
    Many2many y para el ejercicio 25 (crear sus vistas y su menú).
    """

    _name = 'cd.library.genre'
    _description = 'Género de biblioteca'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color')
