from odoo.tests import TransactionCase, tagged


@tagged('cd_restaurant_practice', '-standard')
class TestRelations(TransactionCase):
    """Bloque 3 · Relaciones y ORM avanzada (ejercicios 19 a 24)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Dish = cls.env['cd.restaurant.dish']
        cls.Allergen = cls.env['cd.restaurant.allergen']

    def test_ex19_add_ingredients(self):
        dish = self.Dish.create({'name': 'Con ingredientes'})
        ingredients = dish.exercise_19_add_ingredients(['Tomate', 'Queso'])
        self.assertEqual(
            len(ingredients), 2, 'EJERCICIO 19: debe devolver los 2 ingredientes creados',
        )
        self.assertEqual(
            set(dish.ingredient_ids.mapped('name')), {'Tomate', 'Queso'},
            'EJERCICIO 19: Command.create debe crear los ingredientes en ingredient_ids',
        )

    def test_ex20_set_and_clear_allergens(self):
        dish = self.Dish.create({'name': 'Con alérgenos'})
        dish.exercise_20_set_allergens(['Gluten', 'Lactosa'])
        self.assertEqual(
            set(dish.allergen_ids.mapped('name')), {'Gluten', 'Lactosa'},
            'EJERCICIO 20a: Command.set debe crear y enlazar los alérgenos',
        )
        dish.exercise_20_set_allergens(['Frutos secos'])
        self.assertEqual(
            dish.allergen_ids.mapped('name'), ['Frutos secos'],
            'EJERCICIO 20a: set debe reemplazar los alérgenos, no acumularlos',
        )
        self.assertTrue(
            dish.exercise_20_clear_allergens(), 'EJERCICIO 20b: debe devolver True',
        )
        self.assertFalse(dish.allergen_ids, 'EJERCICIO 20b: Command.clear debe quitarlos todos')

    def test_ex21_inherits_waiter(self):
        self.assertIn(
            'cd.restaurant.waiter', self.env,
            'EJERCICIO 21: falta el modelo cd.restaurant.waiter',
        )
        waiter = self.env['cd.restaurant.waiter'].create({
            'name': 'Ana Camarera',
            'waiter_code': 'W001',
        })
        self.assertTrue(waiter.partner_id, 'EJERCICIO 21: _inherits debe crear el res.partner')
        self.assertEqual(waiter.partner_id.name, 'Ana Camarera')
        waiter.partner_id.name = 'Ana Cambiada'
        self.assertEqual(
            waiter.name, 'Ana Cambiada',
            'EJERCICIO 21: los campos delegados deben sincronizarse',
        )

    def test_ex22_allergen_names_inverse(self):
        self.assertIn(
            'allergen_names', self.Dish._fields,
            'EJERCICIO 22: falta el campo allergen_names',
        )
        allergen_a = self.Allergen.create({'name': 'A'})
        allergen_b = self.Allergen.create({'name': 'B'})
        dish = self.Dish.create({
            'name': 'Nombres',
            'allergen_ids': [(6, 0, (allergen_a + allergen_b).ids)],
        })
        self.assertEqual(
            dish.allergen_names, 'A, B',
            'EJERCICIO 22: el compute debe unir los nombres con ", "',
        )
        dish.allergen_names = 'C, A'
        self.assertEqual(
            set(dish.allergen_ids.mapped('name')), {'C', 'A'},
            'EJERCICIO 22: el inverse debe crear/relacionar los alérgenos indicados',
        )

    def test_ex23_read_group(self):
        self.Dish.with_context(active_test=False).search([]).unlink()
        self.Dish.create({'name': 'D1'})
        self.Dish.create({'name': 'D2'})
        self.Dish.create({'name': 'A1', 'state': 'available'})
        result = dict(self.Dish.exercise_23_read_group_by_state())
        self.assertEqual(result.get('draft'), 2, 'EJERCICIO 23: deben contarse 2 borradores')
        self.assertEqual(result.get('available'), 1, 'EJERCICIO 23: debe contarse 1 disponible')

    def test_ex24_search_fetch(self):
        self.Dish.with_context(active_test=False).search([]).unlink()
        self.Dish.create({'name': 'A', 'state': 'available', 'price': 5.0})
        self.Dish.create({'name': 'B', 'state': 'available', 'price': 15.0})
        self.Dish.create({'name': 'C', 'state': 'draft', 'price': 50.0})
        dishes = self.Dish.exercise_24_search_fetch_available()
        self.assertEqual(
            dishes.mapped('name'), ['B', 'A'],
            'EJERCICIO 24: search_fetch de disponibles ordenados por precio desc',
        )
