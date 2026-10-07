from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase, tagged
from odoo.tools import mute_logger


@tagged('cd_restaurant_practice', '-standard')
class TestFields(TransactionCase):
    """Bloque 2 · Campos y decoradores (ejercicios 9 a 18)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Dish = cls.env['cd.restaurant.dish']
        cls.Ingredient = cls.env['cd.restaurant.ingredient']

    def _assert_field(self, model, field_name, exercise):
        self.assertIn(
            field_name,
            model._fields,
            f'{exercise}: falta el campo {field_name} en {model._name}',
        )

    def test_ex09_price_with_tax(self):
        self._assert_field(self.Dish, 'price_with_tax', 'EJERCICIO 9')
        dish = self.Dish.create({'name': 'IVA', 'price': 100.0})
        self.assertAlmostEqual(
            dish.price_with_tax, 121.0, places=2,
            msg='EJERCICIO 9: 100 con 21% de IVA debe ser 121',
        )
        dish.price = 200.0
        self.assertAlmostEqual(
            dish.price_with_tax, 242.0, places=2,
            msg='EJERCICIO 9: el campo almacenado debe recalcularse al cambiar el precio',
        )

    def test_ex10_price_with_markup(self):
        self._assert_field(self.Dish, 'price_with_markup', 'EJERCICIO 10')
        dish = self.Dish.create({'name': 'Margen', 'price': 100.0})
        self.assertAlmostEqual(
            dish.price_with_markup, 100.0, places=2,
            msg='EJERCICIO 10: sin restaurant_markup en el contexto debe valer price',
        )
        self.assertAlmostEqual(
            dish.with_context(restaurant_markup=50).price_with_markup, 150.0, places=2,
            msg='EJERCICIO 10: con restaurant_markup=50 debe valer 150',
        )

    def test_ex11_related_chef(self):
        self._assert_field(self.Ingredient, 'chef_id', 'EJERCICIO 11')
        partner = self.env['res.partner'].create({'name': 'Chef'})
        dish = self.Dish.create({'name': 'Con chef', 'chef_id': partner.id})
        ingredient = self.Ingredient.create({'name': 'Ingrediente', 'dish_id': dish.id})
        self.assertEqual(
            ingredient.chef_id, partner,
            'EJERCICIO 11: chef_id del ingrediente debe ser el chef del plato',
        )

    def test_ex12_onchange_chef(self):
        with Form(self.Dish) as form:
            form.name = 'Formulario'
            form.chef_id = self.env['res.partner'].create({'name': 'Ana'})
            self.assertEqual(
                form.description, 'Plato de Ana',
                'EJERCICIO 12: el onchange debe rellenar description',
            )

    def test_ex13_constrains_price(self):
        dish = self.Dish.create({'name': 'Precios'})
        with self.assertRaises(ValidationError):
            dish.price = -1.0

    def test_ex14_constraint_quantity(self):
        with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'):
            self.Dish.create({'name': 'Raciones negativas', 'quantity': -1})

    def test_ex15_reference_default(self):
        self._assert_field(self.Dish, 'reference', 'EJERCICIO 15')
        dish = self.Dish.create({'name': 'Referencia'})
        self.assertRegex(
            dish.reference or '',
            r'^PLA/\d{4}$',
            'EJERCICIO 15: reference debe tener el formato PLA/AAAA',
        )

    def test_ex16_display_name(self):
        dish = self.Dish.create({'name': 'Display', 'quantity': 3})
        self.assertEqual(
            dish.display_name, 'Display [3 raciones]',
            'EJERCICIO 16: display_name debe ser "{name} [{quantity} raciones]"',
        )

    def test_ex17_copy_override(self):
        dish = self.Dish.create({'name': 'Original', 'state': 'available', 'quantity': 5})
        copy = dish.copy()
        self.assertEqual(copy.state, 'draft', 'EJERCICIO 17: la copia debe quedar en borrador')
        self.assertEqual(copy.quantity, 1, 'EJERCICIO 17: la copia debe tener 1 ración')

    def test_ex18_active_and_order(self):
        self._assert_field(self.Dish, 'active', 'EJERCICIO 18')
        cheap = self.Dish.create({'name': 'Barato', 'price': 10.0})
        expensive = self.Dish.create({'name': 'Caro', 'price': 30.0})
        middle = self.Dish.create({'name': 'Medio', 'price': 20.0})
        ids = (cheap + expensive + middle).ids
        found = self.Dish.search([('id', 'in', ids)])
        self.assertEqual(
            found.mapped('name'), ['Caro', 'Medio', 'Barato'],
            "EJERCICIO 18: _order = 'price desc, name'",
        )
        cheap.active = False
        self.assertNotIn(cheap, self.Dish.search([('id', 'in', ids)]))
        self.assertIn(
            cheap,
            self.Dish.with_context(active_test=False).search([('id', 'in', ids)]),
            'EJERCICIO 18: sin active_test el registro archivado debe aparecer',
        )
