from odoo import fields, models


class CdRestaurantAllergen(models.Model):
    """Alérgeno de laboratorio (gluten, lactosa, frutos secos...).

    No tiene ejercicios propios: es el comodín para practicar relaciones
    Many2many y para el ejercicio 25 (crear sus vistas y su menú).
    """

    _name = 'cd.restaurant.allergen'
    _description = 'Alérgeno de restaurante'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color')
