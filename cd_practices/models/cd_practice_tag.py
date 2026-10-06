from odoo import fields, models


class CdPracticeTag(models.Model):
    """Etiqueta de laboratorio.

    No tiene ejercicios propios: es el comodín para practicar relaciones
    Many2many y para el ejercicio 25 (crear sus vistas y su menú).
    """

    _name = 'cd.practice.tag'
    _description = 'Etiqueta de prácticas'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color')
