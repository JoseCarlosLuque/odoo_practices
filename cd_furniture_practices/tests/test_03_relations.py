from odoo.tests import TransactionCase, tagged


@tagged('cd_furniture_practice', '-standard')
class TestRelations(TransactionCase):
    """Bloque 3 · Relaciones y ORM avanzada (ejercicios 19 a 24)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['cd.furniture.product']
        cls.Material = cls.env['cd.furniture.material']

    def test_ex19_add_components(self):
        product = self.Product.create({'name': 'Con componentes'})
        components = product.exercise_19_add_components(['Tablero superior', 'Pata'])
        self.assertEqual(
            len(components), 2, 'EJERCICIO 19: debe devolver los 2 componentes creados',
        )
        self.assertEqual(
            set(product.component_ids.mapped('name')), {'Tablero superior', 'Pata'},
            'EJERCICIO 19: Command.create debe crear los componentes en component_ids',
        )

    def test_ex20_set_and_clear_materials(self):
        product = self.Product.create({'name': 'Con materiales'})
        product.exercise_20_set_materials(['Roble', 'Pino'])
        self.assertEqual(
            set(product.material_ids.mapped('name')), {'Roble', 'Pino'},
            'EJERCICIO 20a: Command.set debe crear y enlazar los materiales',
        )
        product.exercise_20_set_materials(['Metal'])
        self.assertEqual(
            product.material_ids.mapped('name'), ['Metal'],
            'EJERCICIO 20a: set debe reemplazar los materiales, no acumularlos',
        )
        self.assertTrue(
            product.exercise_20_clear_materials(), 'EJERCICIO 20b: debe devolver True',
        )
        self.assertFalse(product.material_ids, 'EJERCICIO 20b: Command.clear debe quitarlos todos')

    def test_ex21_inherits_carpenter(self):
        self.assertIn(
            'cd.furniture.carpenter', self.env,
            'EJERCICIO 21: falta el modelo cd.furniture.carpenter',
        )
        carpenter = self.env['cd.furniture.carpenter'].create({
            'name': 'Ana Carpintera',
            'carpenter_code': 'C001',
        })
        self.assertTrue(
            carpenter.partner_id, 'EJERCICIO 21: _inherits debe crear el res.partner',
        )
        self.assertEqual(carpenter.partner_id.name, 'Ana Carpintera')
        carpenter.partner_id.name = 'Ana Cambiada'
        self.assertEqual(
            carpenter.name, 'Ana Cambiada',
            'EJERCICIO 21: los campos delegados deben sincronizarse',
        )

    def test_ex22_material_names_inverse(self):
        self.assertIn(
            'material_names', self.Product._fields,
            'EJERCICIO 22: falta el campo material_names',
        )
        material_a = self.Material.create({'name': 'A'})
        material_b = self.Material.create({'name': 'B'})
        product = self.Product.create({
            'name': 'Nombres',
            'material_ids': [(6, 0, (material_a + material_b).ids)],
        })
        self.assertEqual(
            product.material_names, 'A, B',
            'EJERCICIO 22: el compute debe unir los nombres con ", "',
        )
        product.material_names = 'C, A'
        self.assertEqual(
            set(product.material_ids.mapped('name')), {'C', 'A'},
            'EJERCICIO 22: el inverse debe crear/relacionar los materiales indicados',
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
            'EJERCICIO 24: search_fetch de disponibles ordenados por coste desc',
        )
