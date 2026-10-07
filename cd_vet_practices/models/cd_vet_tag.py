from odoo import fields, models


class CdVetTag(models.Model):
    """Etiqueta de laboratorio (especie, raza, alergia...).

    No tiene ejercicios propios: es el comodín para practicar relaciones
    Many2many y para el ejercicio 25 (crear sus vistas y su menú).
    """

    _name = 'cd.vet.tag'
    _description = 'Etiqueta veterinaria'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color')
