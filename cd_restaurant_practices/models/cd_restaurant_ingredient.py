from odoo import fields, models


class CdRestaurantIngredient(models.Model):
    """Ingrediente de un plato. Se usa en los ejercicios de relaciones (bloque 3)."""

    _name = 'cd.restaurant.ingredient'
    _description = 'Ingrediente de plato'

    name = fields.Char(string='Ingrediente', required=True)
    dish_id = fields.Many2one(
        'cd.restaurant.dish',
        string='Plato',
        required=True,
        ondelete='cascade',
    )
    quantity = fields.Integer(string='Cantidad', default=1)
    price_unit = fields.Float(string='Coste unitario')

    # =========================================================================
    # EJERCICIO 11 · Bloque 2 · Test: TestFields.test_ex11_related_chef
    # -------------------------------------------------------------------------
    # Crea en ESTE modelo un campo chef_id (Many2one a res.partner) que sea
    # un campo related de dish_id.chef_id, sin almacenar.
    # PISTA DE SINTAXIS
    #   chef_id = fields.Many2one(
    #       'res.partner',
    #       string='Chef',
    #       related='dish_id.chef_id',
    #       store=False,
    #   )
    # El test comprueba que ingrediente.chef_id == plato.chef_id.
    # =========================================================================
