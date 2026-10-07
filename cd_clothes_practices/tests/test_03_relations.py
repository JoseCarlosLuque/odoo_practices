from odoo.tests import TransactionCase, tagged


@tagged('cd_clothes_practice', '-standard')
class TestRelations(TransactionCase):
    """Bloque 3 · Relaciones y ORM avanzada (ejercicios 19 a 24)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['cd.clothes.product']
        cls.Category = cls.env['cd.clothes.category']

    def test_ex19_add_variants(self):
        product = self.Product.create({'name': 'Con variantes'})
        variants = product.exercise_19_add_variants(['Talla S', 'Talla M'])
        self.assertEqual(
            len(variants), 2, 'EJERCICIO 19: debe devolver las 2 variantes creadas',
        )
        self.assertEqual(
            set(product.variant_ids.mapped('name')), {'Talla S', 'Talla M'},
            'EJERCICIO 19: Command.create debe crear las variantes en variant_ids',
        )

    def test_ex20_set_and_clear_categories(self):
        product = self.Product.create({'name': 'Con categorías'})
        product.exercise_20_set_categories(['Camisetas', 'Pantalones'])
        self.assertEqual(
            set(product.category_ids.mapped('name')), {'Camisetas', 'Pantalones'},
            'EJERCICIO 20a: Command.set debe crear y enlazar las categorías',
        )
        product.exercise_20_set_categories(['Abrigos'])
        self.assertEqual(
            product.category_ids.mapped('name'), ['Abrigos'],
            'EJERCICIO 20a: set debe reemplazar las categorías, no acumularlas',
        )
        self.assertTrue(
            product.exercise_20_clear_categories(), 'EJERCICIO 20b: debe devolver True',
        )
        self.assertFalse(product.category_ids, 'EJERCICIO 20b: Command.clear debe quitarlas todas')

    def test_ex21_inherits_customer(self):
        self.assertIn(
            'cd.clothes.customer', self.env,
            'EJERCICIO 21: falta el modelo cd.clothes.customer',
        )
        customer = self.env['cd.clothes.customer'].create({
            'name': 'Ana Clienta',
            'customer_code': 'C001',
        })
        self.assertTrue(customer.partner_id, 'EJERCICIO 21: _inherits debe crear el res.partner')
        self.assertEqual(customer.partner_id.name, 'Ana Clienta')
        customer.partner_id.name = 'Ana Cambiada'
        self.assertEqual(
            customer.name, 'Ana Cambiada',
            'EJERCICIO 21: los campos delegados deben sincronizarse',
        )

    def test_ex22_category_names_inverse(self):
        self.assertIn(
            'category_names', self.Product._fields,
            'EJERCICIO 22: falta el campo category_names',
        )
        category_a = self.Category.create({'name': 'A'})
        category_b = self.Category.create({'name': 'B'})
        product = self.Product.create({
            'name': 'Nombres',
            'category_ids': [(6, 0, (category_a + category_b).ids)],
        })
        self.assertEqual(
            product.category_names, 'A, B',
            'EJERCICIO 22: el compute debe unir los nombres con ", "',
        )
        product.category_names = 'C, A'
        self.assertEqual(
            set(product.category_ids.mapped('name')), {'C', 'A'},
            'EJERCICIO 22: el inverse debe crear/relacionar las categorías indicadas',
        )

    def test_ex23_read_group(self):
        self.Product.with_context(active_test=False).search([]).unlink()
        self.Product.create({'name': 'D1'})
        self.Product.create({'name': 'D2'})
        self.Product.create({'name': 'A1', 'state': 'available'})
        result = dict(self.Product.exercise_23_read_group_by_state())
        self.assertEqual(result.get('draft'), 2, 'EJERCICIO 23: deben contarse 2 borradores')
        self.assertEqual(result.get('available'), 1, 'EJERCICIO 23: debe contarse 1 disponible')

    def test_ex24_search_fetch(self):
        self.Product.with_context(active_test=False).search([]).unlink()
        self.Product.create({'name': 'A', 'state': 'available', 'price': 5.0})
        self.Product.create({'name': 'B', 'state': 'available', 'price': 15.0})
        self.Product.create({'name': 'C', 'state': 'draft', 'price': 50.0})
        products = self.Product.exercise_24_search_fetch_available()
        self.assertEqual(
            products.mapped('name'), ['B', 'A'],
            'EJERCICIO 24: search_fetch de disponibles ordenadas por precio desc',
        )
