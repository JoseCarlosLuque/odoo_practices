from odoo.tests import TransactionCase, tagged


@tagged('cd_restaurant_practice', '-standard')
class TestOrmBasics(TransactionCase):
    """Bloque 1 · ORM básica (ejercicios 1 a 8)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Dish = cls.env['cd.restaurant.dish']

    def _create_dish(self, name, **vals):
        return self.Dish.create({'name': name, **vals})

    def test_ex01_create_dishes(self):
        dishes = self.Dish.exercise_01_create_dishes()
        self.assertEqual(len(dishes), 3, 'EJERCICIO 1: create() debe devolver 3 platos')
        by_name = {dish.name: dish for dish in dishes}
        self.assertEqual(
            set(by_name),
            {'Plato A', 'Plato B', 'Plato C'},
            'EJERCICIO 1: los nombres deben ser Plato A, Plato B y Plato C',
        )
        self.assertAlmostEqual(
            by_name['Plato A'].price, 10.0, msg='EJERCICIO 1: precio de Plato A',
        )
        self.assertAlmostEqual(
            by_name['Plato B'].price, 20.0, msg='EJERCICIO 1: precio de Plato B',
        )
        self.assertAlmostEqual(
            by_name['Plato C'].price, 30.0, msg='EJERCICIO 1: precio de Plato C',
        )

    def test_ex02_search_dishes(self):
        # Limpia datos preexistentes (p. ej. demo) para que el test sea
        # determinista; el cambio se revierte al terminar (TransactionCase).
        self.Dish.with_context(active_test=False).search([]).unlink()
        self._create_dish('Barato', price=5.0)
        self._create_dish('Medio', price=10.0)
        self._create_dish('Caro', price=15.0)
        self._create_dish('Muy caro', price=20.0)
        dishes = self.Dish.exercise_02_search_dishes(10.0, 2)
        self.assertEqual(
            dishes.mapped('name'),
            ['Muy caro', 'Caro'],
            'EJERCICIO 2: dominio precio >= 10, orden precio desc y limit 2',
        )

    def test_ex03_count_by_chef(self):
        ana = self.env['res.partner'].create({'name': 'Ana'})
        bruno = self.env['res.partner'].create({'name': 'Bruno'})
        self._create_dish('A1', chef_id=ana.id)
        self._create_dish('A2', chef_id=ana.id)
        self._create_dish('B1', chef_id=bruno.id)
        self._create_dish('Sin chef')
        self.assertEqual(
            self.Dish.exercise_03_count_dishes_by_chef(ana),
            2,
            'EJERCICIO 3: Ana debe tener 2 platos',
        )
        self.assertEqual(
            self.Dish.exercise_03_count_dishes_by_chef(bruno),
            1,
            'EJERCICIO 3: Bruno debe tener 1 plato',
        )

    def test_ex04_expensive_names(self):
        self.Dish.with_context(active_test=False).search([]).unlink()
        self._create_dish('Zeta', price=5.0)
        self._create_dish('Alfa', price=15.0)
        self._create_dish('Media', price=25.0)
        names = self.Dish.exercise_04_expensive_dish_names(10.0)
        self.assertEqual(
            names,
            ['Alfa', 'Media'],
            'EJERCICIO 4: precio ESTRICTAMENTE mayor que 10 y nombres ordenados alfabéticamente',
        )

    def test_ex05_set_state(self):
        a = self._create_dish('A')
        b = self._create_dish('B')
        c = self._create_dish('C')
        count = self.Dish.exercise_05_set_state(['A', 'B'], 'on_menu')
        self.assertEqual(count, 2, 'EJERCICIO 5: debe devolver 2 registros modificados')
        self.assertEqual(a.state, 'on_menu', 'EJERCICIO 5: A debe estar en carta')
        self.assertEqual(b.state, 'on_menu', 'EJERCICIO 5: B debe estar en carta')
        self.assertEqual(c.state, 'draft', 'EJERCICIO 5: C no debe haberse tocado')

    def test_ex06_delete_sold_out(self):
        sold_out = self._create_dish('R1', state='sold_out')
        draft = self._create_dish('D1')
        deleted = self.Dish.exercise_06_delete_sold_out()
        self.assertEqual(deleted, 1, 'EJERCICIO 6: debe borrar 1 plato agotado')
        self.assertFalse(sold_out.exists(), 'EJERCICIO 6: el agotado debe estar borrado')
        self.assertTrue(draft.exists(), 'EJERCICIO 6: el borrador no debe borrarse')

    def test_ex07_complex_domain(self):
        self._create_dish('Alfa', description='contiene orm', price=10.0)
        self._create_dish('Orme', description='otra cosa', price=12.0)
        self._create_dish('Beta', description='contiene orm', price=5.0)
        self._create_dish('Gamma', description='nada', price=50.0)
        names = self.Dish.exercise_07_complex_domain('orm', 10.0)
        self.assertEqual(
            sorted(names),
            ['Alfa', 'Orme'],
            'EJERCICIO 7: (name ilike orm o description ilike orm) y precio >= 10',
        )

    def test_ex08_browse_vs_search(self):
        dish = self._create_dish('Existe')
        result = self.Dish.exercise_08_browse_vs_search([dish.id, 999999])
        self.assertEqual(result.get('found'), 1, "EJERCICIO 8: 'found' debe contar los que existen")
        self.assertEqual(
            result.get('missing'),
            [999999],
            "EJERCICIO 8: 'missing' debe contener los ids inexistentes",
        )
