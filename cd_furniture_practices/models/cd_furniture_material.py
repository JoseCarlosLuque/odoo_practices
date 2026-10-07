from odoo import fields, models


class CdFurnitureMaterial(models.Model):
    """Material de laboratorio (roble, pino, metal...).

    No tiene ejercicios propios: es el comodín para practicar relaciones
    Many2many y para el ejercicio 25 (crear sus vistas y su menú).
    """

    _name = 'cd.furniture.material'
    _description = 'Material de fábrica'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color')
