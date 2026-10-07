from odoo.tests import TransactionCase, tagged


@tagged('cd_gym_practice', '-standard')
class TestRelations(TransactionCase):
    """Bloque 3 · Relaciones y ORM avanzada (ejercicios 19 a 24)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Membership = cls.env['cd.gym.membership']
        cls.Activity = cls.env['cd.gym.activity']

    def test_ex19_add_services(self):
        membership = self.Membership.create({'name': 'Con servicios'})
        services = membership.exercise_19_add_services(['Entrenamiento personal', 'Piscina'])
        self.assertEqual(
            len(services), 2, 'EJERCICIO 19: debe devolver los 2 servicios creados',
        )
        self.assertEqual(
            set(membership.service_ids.mapped('name')),
            {'Entrenamiento personal', 'Piscina'},
            'EJERCICIO 19: Command.create debe crear los servicios en service_ids',
        )

    def test_ex20_set_and_clear_activities(self):
        membership = self.Membership.create({'name': 'Con actividades'})
        membership.exercise_20_set_activities(['Yoga', 'Crossfit'])
        self.assertEqual(
            set(membership.activity_ids.mapped('name')), {'Yoga', 'Crossfit'},
            'EJERCICIO 20a: Command.set debe crear y enlazar las actividades',
        )
        membership.exercise_20_set_activities(['Pilates'])
        self.assertEqual(
            membership.activity_ids.mapped('name'), ['Pilates'],
            'EJERCICIO 20a: set debe reemplazar las actividades, no acumularlas',
        )
        self.assertTrue(
            membership.exercise_20_clear_activities(), 'EJERCICIO 20b: debe devolver True',
        )
        self.assertFalse(membership.activity_ids, 'EJERCICIO 20b: Command.clear debe quitarlas todas')

    def test_ex21_inherits_member(self):
        self.assertIn(
            'cd.gym.member', self.env,
            'EJERCICIO 21: falta el modelo cd.gym.member',
        )
        member = self.env['cd.gym.member'].create({
            'name': 'Ana Miembro',
            'member_code': 'M001',
        })
        self.assertTrue(member.partner_id, 'EJERCICIO 21: _inherits debe crear el res.partner')
        self.assertEqual(member.partner_id.name, 'Ana Miembro')
        member.partner_id.name = 'Ana Cambiada'
        self.assertEqual(
            member.name, 'Ana Cambiada',
            'EJERCICIO 21: los campos delegados deben sincronizarse',
        )

    def test_ex22_activity_names_inverse(self):
        self.assertIn(
            'activity_names', self.Membership._fields,
            'EJERCICIO 22: falta el campo activity_names',
        )
        activity_a = self.Activity.create({'name': 'A'})
        activity_b = self.Activity.create({'name': 'B'})
        membership = self.Membership.create({
            'name': 'Nombres',
            'activity_ids': [(6, 0, (activity_a + activity_b).ids)],
        })
        self.assertEqual(
            membership.activity_names, 'A, B',
            'EJERCICIO 22: el compute debe unir los nombres con ", "',
        )
        membership.activity_names = 'C, A'
        self.assertEqual(
            set(membership.activity_ids.mapped('name')), {'C', 'A'},
            'EJERCICIO 22: el inverse debe crear/relacionar las actividades indicadas',
        )

    def test_ex23_read_group(self):
        self.Membership.with_context(active_test=False).search([]).unlink()
        self.Membership.create({'name': 'D1'})
        self.Membership.create({'name': 'D2'})
        self.Membership.create({'name': 'A1', 'state': 'active'})
        result = dict(self.Membership.exercise_23_read_group_by_state())
        self.assertEqual(result.get('draft'), 2, 'EJERCICIO 23: deben contarse 2 borradores')
        self.assertEqual(result.get('active'), 1, 'EJERCICIO 23: debe contarse 1 activa')

    def test_ex24_search_fetch(self):
        self.Membership.with_context(active_test=False).search([]).unlink()
        self.Membership.create({'name': 'A', 'state': 'active', 'price': 5.0})
        self.Membership.create({'name': 'B', 'state': 'active', 'price': 15.0})
        self.Membership.create({'name': 'C', 'state': 'draft', 'price': 50.0})
        memberships = self.Membership.exercise_24_search_fetch_active()
        self.assertEqual(
            memberships.mapped('name'), ['B', 'A'],
            'EJERCICIO 24: search_fetch de activas ordenadas por precio desc',
        )
