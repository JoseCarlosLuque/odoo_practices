from odoo.tests import TransactionCase, tagged


@tagged('cd_clothes_practice', '-standard')
class TestOrmBasics(TransactionCase):
    """Bloque 1 · ORM básica (ejercicios 1 a 8)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['cd.clothes.product']

    def _create_product(self, name, **vals):
        return self.Product.create({'name': name, **vals})

    def test_ex01_create_products(self):
        products = self.Product.exercise_01_create_products()
        self.assertEqual(len(products), 3, 'EJERCICIO 1: create() debe devolver 3 prendas')
        by_name = {product.name: product for product in products}
        self.assertEqual(
            set(by_name),
            {'Prenda A', 'Prenda B', 'Prenda C'},
            'EJERCICIO 1: los nombres deben ser Prenda A, Prenda B y Prenda C',
        )
        self.assertAlmostEqual(
            by_name['Prenda A'].price, 10.0, msg='EJERCICIO 1: precio de Prenda A',
        )
        self.assertAlmostEqual(
            by_name['Prenda B'].price, 20.0, msg='EJERCICIO 1: precio de Prenda B',
        )
        self.assertAlmostEqual(
            by_name['Prenda C'].price, 30.0, msg='EJERCICIO 1: precio de Prenda C',
        )

    def test_ex02_search_products(self):
        # Limpia datos preexistentes (p. ej. demo) para que el test sea
        # determinista; el cambio se revierte al terminar (TransactionCase).
        self.Product.with_context(active_test=False).search([]).unlink()
        self._create_product('Barata', price=5.0)
        self._create_product('Media', price=10.0)
        self._create_product('Cara', price=15.0)
        self._create_product('Muy cara', price=20.0)
        products = self.Product.exercise_02_search_products(10.0, 2)
        self.assertEqual(
            products.mapped('name'),
            ['Muy cara', 'Cara'],
            'EJERCICIO 2: dominio precio >= 10, orden precio desc y limit 2',
        )

    def test_ex03_count_by_supplier(self):
        ana = self.env['res.partner'].create({'name': 'Ana'})
        bruno = self.env['res.partner'].create({'name': 'Bruno'})
        self._create_product('A1', supplier_id=ana.id)
        self._create_product('A2', supplier_id=ana.id)
        self._create_product('B1', supplier_id=bruno.id)
        self._create_product('Sin proveedor')
        self.assertEqual(
            self.Product.exercise_03_count_products_by_supplier(ana),
            2,
            'EJERCICIO 3: Ana debe tener 2 prendas',
        )
        self.assertEqual(
            self.Product.exercise_03_count_products_by_supplier(bruno),
            1,
            'EJERCICIO 3: Bruno debe tener 1 prenda',
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
            'EJERCICIO 4: precio ESTRICTAMENTE mayor que 10 y nombres ordenados alfabéticamente',
        )

    def test_ex05_set_state(self):
        a = self._create_product('A')
        b = self._create_product('B')
        c = self._create_product('C')
        count = self.Product.exercise_05_set_state(['A', 'B'], 'on_sale')
        self.assertEqual(count, 2, 'EJERCICIO 5: debe devolver 2 registros modificados')
        self.assertEqual(a.state, 'on_sale', 'EJERCICIO 5: A debe estar en oferta')
        self.assertEqual(b.state, 'on_sale', 'EJERCICIO 5: B debe estar en oferta')
        self.assertEqual(c.state, 'draft', 'EJERCICIO 5: C no debe haberse tocado')

    def test_ex06_delete_sold_out(self):
        sold_out = self._create_product('R1', state='sold_out')
        draft = self._create_product('D1')
        deleted = self.Product.exercise_06_delete_sold_out()
        self.assertEqual(deleted, 1, 'EJERCICIO 6: debe borrar 1 prenda agotada')
        self.assertFalse(sold_out.exists(), 'EJERCICIO 6: la agotada debe estar borrada')
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
            'EJERCICIO 7: (name ilike orm o description ilike orm) y precio >= 10',
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
