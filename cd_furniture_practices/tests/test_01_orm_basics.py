from odoo.tests import TransactionCase, tagged


@tagged('cd_furniture_practice', '-standard')
class TestOrmBasics(TransactionCase):
    """Bloque 1 · ORM básica (ejercicios 1 a 8)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['cd.furniture.product']

    def _create_product(self, name, **vals):
        return self.Product.create({'name': name, **vals})

    def test_ex01_create_products(self):
        products = self.Product.exercise_01_create_products()
        self.assertEqual(len(products), 3, 'EJERCICIO 1: create() debe devolver 3 muebles')
        by_name = {product.name: product for product in products}
        self.assertEqual(
            set(by_name),
            {'Mueble A', 'Mueble B', 'Mueble C'},
            'EJERCICIO 1: los nombres deben ser Mueble A, Mueble B y Mueble C',
        )
        self.assertAlmostEqual(
            by_name['Mueble A'].price, 10.0, msg='EJERCICIO 1: coste de Mueble A',
        )
        self.assertAlmostEqual(
            by_name['Mueble B'].price, 20.0, msg='EJERCICIO 1: coste de Mueble B',
        )
        self.assertAlmostEqual(
            by_name['Mueble C'].price, 30.0, msg='EJERCICIO 1: coste de Mueble C',
        )

    def test_ex02_search_products(self):
        # Limpia datos preexistentes (p. ej. demo) para que el test sea
        # determinista; el cambio se revierte al terminar (TransactionCase).
        self.Product.with_context(active_test=False).search([]).unlink()
        self._create_product('Barato', price=5.0)
        self._create_product('Medio', price=10.0)
        self._create_product('Caro', price=15.0)
        self._create_product('Muy caro', price=20.0)
        products = self.Product.exercise_02_search_products(10.0, 2)
        self.assertEqual(
            products.mapped('name'),
            ['Muy caro', 'Caro'],
            'EJERCICIO 2: dominio coste >= 10, orden coste desc y limit 2',
        )

    def test_ex03_count_by_designer(self):
        ana = self.env['res.partner'].create({'name': 'Ana'})
        bruno = self.env['res.partner'].create({'name': 'Bruno'})
        self._create_product('A1', designer_id=ana.id)
        self._create_product('A2', designer_id=ana.id)
        self._create_product('B1', designer_id=bruno.id)
        self._create_product('Sin diseñador')
        self.assertEqual(
            self.Product.exercise_03_count_products_by_designer(ana),
            2,
            'EJERCICIO 3: Ana debe tener 2 muebles',
        )
        self.assertEqual(
            self.Product.exercise_03_count_products_by_designer(bruno),
            1,
            'EJERCICIO 3: Bruno debe tener 1 mueble',
        )

    def test_ex04_expensive_names(self):
        self.Product.with_context(active_test=False).search([]).unlink()
        self._create_product('Zeta', price=5.0)
        self._create_product('Alfa', price=15.0)
        self._create_product('Media', price=25.0)
        names = self.Product.exercise_04_expensive_product_names(10.0)
        self.assertEqual(
            names,
            ['Alfa', 'Media'],
            'EJERCICIO 4: coste ESTRICTAMENTE mayor que 10 y nombres ordenados alfabéticamente',
        )

    def test_ex05_set_state(self):
        a = self._create_product('A')
        b = self._create_product('B')
        c = self._create_product('C')
        count = self.Product.exercise_05_set_state(['A', 'B'], 'in_production')
        self.assertEqual(count, 2, 'EJERCICIO 5: debe devolver 2 registros modificados')
        self.assertEqual(a.state, 'in_production', 'EJERCICIO 5: A debe estar en producción')
        self.assertEqual(b.state, 'in_production', 'EJERCICIO 5: B debe estar en producción')
        self.assertEqual(c.state, 'draft', 'EJERCICIO 5: C no debe haberse tocado')

    def test_ex06_delete_archived(self):
        archived = self._create_product('R1', state='archived')
        draft = self._create_product('D1')
        deleted = self.Product.exercise_06_delete_archived()
        self.assertEqual(deleted, 1, 'EJERCICIO 6: debe borrar 1 mueble archivado')
        self.assertFalse(archived.exists(), 'EJERCICIO 6: el archivado debe estar borrado')
        self.assertTrue(draft.exists(), 'EJERCICIO 6: el borrador no debe borrarse')

    def test_ex07_complex_domain(self):
        self._create_product('Alfa', description='contiene orm', price=10.0)
        self._create_product('Orme', description='otra cosa', price=12.0)
        self._create_product('Beta', description='contiene orm', price=5.0)
        self._create_product('Gamma', description='nada', price=50.0)
        names = self.Product.exercise_07_complex_domain('orm', 10.0)
        self.assertEqual(
            sorted(names),
            ['Alfa', 'Orme'],
            'EJERCICIO 7: (name ilike orm o description ilike orm) y coste >= 10',
        )

    def test_ex08_browse_vs_search(self):
        product = self._create_product('Existe')
        result = self.Product.exercise_08_browse_vs_search([product.id, 999999])
        self.assertEqual(result.get('found'), 1, "EJERCICIO 8: 'found' debe contar los que existen")
        self.assertEqual(
            result.get('missing'),
            [999999],
            "EJERCICIO 8: 'missing' debe contener los ids inexistentes",
        )
