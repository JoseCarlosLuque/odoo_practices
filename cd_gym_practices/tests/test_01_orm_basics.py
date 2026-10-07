from odoo.tests import TransactionCase, tagged


@tagged('cd_gym_practice', '-standard')
class TestOrmBasics(TransactionCase):
    """Bloque 1 · ORM básica (ejercicios 1 a 8)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Membership = cls.env['cd.gym.membership']

    def _create_membership(self, name, **vals):
        return self.Membership.create({'name': name, **vals})

    def test_ex01_create_memberships(self):
        memberships = self.Membership.exercise_01_create_memberships()
        self.assertEqual(
            len(memberships), 3, 'EJERCICIO 1: create() debe devolver 3 cuotas',
        )
        by_name = {membership.name: membership for membership in memberships}
        self.assertEqual(
            set(by_name),
            {'Cuota A', 'Cuota B', 'Cuota C'},
            'EJERCICIO 1: los nombres deben ser Cuota A, Cuota B y Cuota C',
        )
        self.assertAlmostEqual(
            by_name['Cuota A'].price, 10.0, msg='EJERCICIO 1: precio de Cuota A',
        )
        self.assertAlmostEqual(
            by_name['Cuota B'].price, 20.0, msg='EJERCICIO 1: precio de Cuota B',
        )
        self.assertAlmostEqual(
            by_name['Cuota C'].price, 30.0, msg='EJERCICIO 1: precio de Cuota C',
        )

    def test_ex02_search_memberships(self):
        # Limpia datos preexistentes (p. ej. demo) para que el test sea
        # determinista; el cambio se revierte al terminar (TransactionCase).
        self.Membership.with_context(active_test=False).search([]).unlink()
        self._create_membership('Barata', price=5.0)
        self._create_membership('Media', price=10.0)
        self._create_membership('Cara', price=15.0)
        self._create_membership('Muy cara', price=20.0)
        memberships = self.Membership.exercise_02_search_memberships(10.0, 2)
        self.assertEqual(
            memberships.mapped('name'),
            ['Muy cara', 'Cara'],
            'EJERCICIO 2: dominio precio >= 10, orden precio desc y limit 2',
        )

    def test_ex03_count_by_partner(self):
        ana = self.env['res.partner'].create({'name': 'Ana'})
        bruno = self.env['res.partner'].create({'name': 'Bruno'})
        self._create_membership('A1', partner_id=ana.id)
        self._create_membership('A2', partner_id=ana.id)
        self._create_membership('B1', partner_id=bruno.id)
        self._create_membership('Sin socio')
        self.assertEqual(
            self.Membership.exercise_03_count_memberships_by_partner(ana),
            2,
            'EJERCICIO 3: Ana debe tener 2 cuotas',
        )
        self.assertEqual(
            self.Membership.exercise_03_count_memberships_by_partner(bruno),
            1,
            'EJERCICIO 3: Bruno debe tener 1 cuota',
        )

    def test_ex04_expensive_names(self):
        self.Membership.with_context(active_test=False).search([]).unlink()
        self._create_membership('Zeta', price=5.0)
        self._create_membership('Alfa', price=15.0)
        self._create_membership('Media', price=25.0)
        names = self.Membership.exercise_04_expensive_membership_names(10.0)
        self.assertEqual(
            names,
            ['Alfa', 'Media'],
            'EJERCICIO 4: precio ESTRICTAMENTE mayor que 10 y nombres ordenados alfabéticamente',
        )

    def test_ex05_set_state(self):
        a = self._create_membership('A')
        b = self._create_membership('B')
        c = self._create_membership('C')
        count = self.Membership.exercise_05_set_state(['A', 'B'], 'frozen')
        self.assertEqual(count, 2, 'EJERCICIO 5: debe devolver 2 registros modificados')
        self.assertEqual(a.state, 'frozen', 'EJERCICIO 5: A debe estar congelada')
        self.assertEqual(b.state, 'frozen', 'EJERCICIO 5: B debe estar congelada')
        self.assertEqual(c.state, 'draft', 'EJERCICIO 5: C no debe haberse tocado')

    def test_ex06_delete_cancelled(self):
        cancelled = self._create_membership('R1', state='cancelled')
        draft = self._create_membership('D1')
        deleted = self.Membership.exercise_06_delete_cancelled()
        self.assertEqual(deleted, 1, 'EJERCICIO 6: debe borrar 1 cuota cancelada')
        self.assertFalse(cancelled.exists(), 'EJERCICIO 6: la cancelada debe estar borrada')
        self.assertTrue(draft.exists(), 'EJERCICIO 6: el borrador no debe borrarse')

    def test_ex07_complex_domain(self):
        self._create_membership('Alfa', description='contiene orm', price=10.0)
        self._create_membership('Orme', description='otra cosa', price=12.0)
        self._create_membership('Beta', description='contiene orm', price=5.0)
        self._create_membership('Gamma', description='nada', price=50.0)
        names = self.Membership.exercise_07_complex_domain('orm', 10.0)
        self.assertEqual(
            sorted(names),
            ['Alfa', 'Orme'],
            'EJERCICIO 7: (name ilike orm o description ilike orm) y precio >= 10',
        )

    def test_ex08_browse_vs_search(self):
        membership = self._create_membership('Existe')
        result = self.Membership.exercise_08_browse_vs_search([membership.id, 999999])
        self.assertEqual(result.get('found'), 1, "EJERCICIO 8: 'found' debe contar los que existen")
        self.assertEqual(
            result.get('missing'),
            [999999],
            "EJERCICIO 8: 'missing' debe contener los ids inexistentes",
        )
