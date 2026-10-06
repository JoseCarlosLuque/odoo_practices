from odoo.tests import TransactionCase, tagged


@tagged('cd_practice', '-standard')
class TestOrmBasics(TransactionCase):
    """Bloque 1 · ORM básica (ejercicios 1 a 8)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Item = cls.env['cd.practice.item']

    def _create_item(self, name, **vals):
        return self.Item.create({'name': name, **vals})

    def test_ex01_create_items(self):
        items = self.Item.exercise_01_create_items()
        self.assertEqual(len(items), 3, 'EJERCICIO 1: create() debe devolver 3 elementos')
        by_name = {item.name: item for item in items}
        self.assertEqual(
            set(by_name),
            {'Item A', 'Item B', 'Item C'},
            'EJERCICIO 1: los nombres deben ser Item A, Item B e Item C',
        )
        self.assertAlmostEqual(by_name['Item A'].price, 10.0, msg='EJERCICIO 1: precio de Item A')
        self.assertAlmostEqual(by_name['Item B'].price, 20.0, msg='EJERCICIO 1: precio de Item B')
        self.assertAlmostEqual(by_name['Item C'].price, 30.0, msg='EJERCICIO 1: precio de Item C')

    def test_ex02_search_items(self):
        self._create_item('Barato', price=5.0)
        self._create_item('Medio', price=10.0)
        self._create_item('Caro', price=15.0)
        self._create_item('Muy caro', price=20.0)
        items = self.Item.exercise_02_search_items(10.0, 2)
        self.assertEqual(
            items.mapped('name'),
            ['Muy caro', 'Caro'],
            'EJERCICIO 2: dominio precio >= 10, orden precio desc y limit 2',
        )

    def test_ex03_count_by_owner(self):
        ana = self.env['res.partner'].create({'name': 'Ana'})
        bruno = self.env['res.partner'].create({'name': 'Bruno'})
        self._create_item('A1', owner_id=ana.id)
        self._create_item('A2', owner_id=ana.id)
        self._create_item('B1', owner_id=bruno.id)
        self._create_item('Sin dueño')
        self.assertEqual(
            self.Item.exercise_03_count_items_by_owner(ana),
            2,
            'EJERCICIO 3: Ana debe tener 2 elementos',
        )
        self.assertEqual(
            self.Item.exercise_03_count_items_by_owner(bruno),
            1,
            'EJERCICIO 3: Bruno debe tener 1 elemento',
        )

    def test_ex04_expensive_names(self):
        self._create_item('Zeta', price=5.0)
        self._create_item('Alfa', price=15.0)
        self._create_item('Media', price=25.0)
        names = self.Item.exercise_04_expensive_item_names(10.0)
        self.assertEqual(
            names,
            ['Alfa', 'Media'],
            'EJERCICIO 4: precio ESTRICTAMENTE mayor que 10 y nombres ordenados alfabéticamente',
        )

    def test_ex05_set_state(self):
        a = self._create_item('A')
        b = self._create_item('B')
        c = self._create_item('C')
        count = self.Item.exercise_05_set_state(['A', 'B'], 'available')
        self.assertEqual(count, 2, 'EJERCICIO 5: debe devolver 2 registros modificados')
        self.assertEqual(a.state, 'available', 'EJERCICIO 5: A debe estar disponible')
        self.assertEqual(b.state, 'available', 'EJERCICIO 5: B debe estar disponible')
        self.assertEqual(c.state, 'draft', 'EJERCICIO 5: C no debe haberse tocado')

    def test_ex06_delete_cancelled(self):
        cancelled = self._create_item('C1', state='cancelled')
        draft = self._create_item('D1')
        deleted = self.Item.exercise_06_delete_cancelled()
        self.assertEqual(deleted, 1, 'EJERCICIO 6: debe borrar 1 elemento cancelado')
        self.assertFalse(cancelled.exists(), 'EJERCICIO 6: el cancelado debe estar borrado')
        self.assertTrue(draft.exists(), 'EJERCICIO 6: el borrador no debe borrarse')

    def test_ex07_complex_domain(self):
        self._create_item('Alfa', description='contiene orm', price=10.0)
        self._create_item('Orme', description='otra cosa', price=12.0)
        self._create_item('Beta', description='contiene orm', price=5.0)
        self._create_item('Gamma', description='nada', price=50.0)
        names = self.Item.exercise_07_complex_domain('orm', 10.0)
        self.assertEqual(
            sorted(names),
            ['Alfa', 'Orme'],
            'EJERCICIO 7: (name ilike orm o description ilike orm) y precio >= 10',
        )

    def test_ex08_browse_vs_search(self):
        item = self._create_item('Existe')
        result = self.Item.exercise_08_browse_vs_search([item.id, 999999])
        self.assertEqual(result.get('found'), 1, "EJERCICIO 8: 'found' debe contar los que existen")
        self.assertEqual(
            result.get('missing'),
            [999999],
            "EJERCICIO 8: 'missing' debe contener los ids inexistentes",
        )
