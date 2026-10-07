from odoo.tests import TransactionCase, tagged


@tagged('cd_gym_practice', '-standard')
class TestViews(TransactionCase):
    """Bloque 4 · Vistas y acciones XML (ejercicios 25 a 29)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Membership = cls.env['cd.gym.membership']

    def _ref(self, xmlid, exercise):
        record = self.env.ref(xmlid, raise_if_not_found=False)
        self.assertTrue(record, f'{exercise}: no existe el xml id {xmlid}')
        return record

    def test_ex25_activity_views(self):
        list_view = self._ref('cd_gym_practices.view_cd_gym_activity_list', 'EJERCICIO 25')
        self.assertEqual(
            list_view.model, 'cd.gym.activity', 'EJERCICIO 25: modelo de la vista list',
        )
        form_view = self._ref('cd_gym_practices.view_cd_gym_activity_form', 'EJERCICIO 25')
        self.assertEqual(
            form_view.model, 'cd.gym.activity', 'EJERCICIO 25: modelo de la vista form',
        )
        action = self._ref('cd_gym_practices.action_cd_gym_activity', 'EJERCICIO 25')
        self.assertEqual(
            action.res_model, 'cd.gym.activity', 'EJERCICIO 25: res_model de la acción',
        )
        self._ref('cd_gym_practices.menu_cd_gym_activity', 'EJERCICIO 25')

    def test_ex26_partner_fields(self):
        Partner = self.env['res.partner']
        self.assertIn(
            'membership_ids', Partner._fields,
            'EJERCICIO 26: falta el campo membership_ids en res.partner',
        )
        self.assertIn(
            'membership_count', Partner._fields,
            'EJERCICIO 26: falta el campo membership_count en res.partner',
        )
        self.assertTrue(
            hasattr(Partner, 'action_view_memberships'),
            'EJERCICIO 26: falta el método action_view_memberships',
        )
        partner = Partner.create({'name': 'Partner gimnasio'})
        self.Membership.create({'name': 'Suya', 'partner_id': partner.id})
        self.assertEqual(
            partner.membership_count, 1,
            'EJERCICIO 26: membership_count debe contar las cuotas del partner',
        )
        action = partner.action_view_memberships()
        self.assertEqual(
            action.get('res_model'), 'cd.gym.membership',
            'EJERCICIO 26: la acción debe abrir cd.gym.membership',
        )
        domain = [tuple(membership) for membership in (action.get('domain') or [])]
        self.assertIn(
            ('partner_id', '=', partner.id), domain,
            'EJERCICIO 26: el dominio debe filtrar por partner_id',
        )

    def test_ex27_partner_view_inherit(self):
        view = self._ref(
            'cd_gym_practices.view_res_partner_form_inherit_gym',
            'EJERCICIO 27',
        )
        arch = view.get_combined_arch()
        self.assertIn('membership_count', arch, 'EJERCICIO 27: añade membership_count')
        self.assertIn('membership_ids', arch, 'EJERCICIO 27: añade membership_ids')
        self.assertIn(
            'action_view_memberships', arch,
            'EJERCICIO 27: añade el botón action_view_memberships',
        )

    def test_ex28_button_and_method(self):
        draft = self.Membership.create({'name': 'Borrador'})
        active = self.Membership.create({'name': 'Activa', 'state': 'active'})
        result = draft.action_mark_active()
        self.assertEqual(
            draft.state, 'active',
            'EJERCICIO 28a: action_mark_active debe pasar de draft a active',
        )
        self.assertEqual(
            active.state, 'active',
            'EJERCICIO 28a: no debe tocar los registros que no están en draft',
        )
        self.assertTrue(result, 'EJERCICIO 28a: debe devolver True')
        view = self.env.ref('cd_gym_practices.view_cd_gym_membership_form')
        arch = view.get_combined_arch()
        self.assertIn(
            'action_mark_active', arch,
            'EJERCICIO 28b: añade el botón action_mark_active en el header de la vista',
        )
        self.assertIn(
            'invisible', arch,
            "EJERCICIO 28b: el botón debe llevar invisible=\"state != 'draft'\"",
        )

    def test_ex29_server_action(self):
        action = self._ref(
            'cd_gym_practices.action_server_reset_membership_state',
            'EJERCICIO 29',
        )
        self.assertEqual(
            action.model_id.model, 'cd.gym.membership',
            'EJERCICIO 29: el server action debe ser del modelo cd.gym.membership',
        )
        membership = self.Membership.create({'name': 'Reset', 'state': 'active'})
        action.with_context(
            active_model='cd.gym.membership',
            active_ids=membership.ids,
        ).run()
        self.assertEqual(
            membership.state, 'draft',
            'EJERCICIO 29: el código del server action debe reiniciar el estado',
        )
