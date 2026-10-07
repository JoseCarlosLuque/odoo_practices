from odoo import fields, models


class CdGymActivity(models.Model):
    """Actividad de laboratorio (yoga, crossfit, natación...).

    No tiene ejercicios propios: es el comodín para practicar relaciones
    Many2many y para el ejercicio 25 (crear sus vistas y su menú).
    """

    _name = 'cd.gym.activity'
    _description = 'Actividad de gimnasio'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color')
