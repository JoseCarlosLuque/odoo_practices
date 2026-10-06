from odoo.tests import TransactionCase, tagged


@tagged('cd_practice', '-standard')
class TestViews(TransactionCase):
    """Bloque 4 · Vistas y acciones XML (ejercicios 25 a 29)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Item = cls.env['cd.practice.item']

    def _ref(self, xmlid, exercise):
        record = self.env.ref(xmlid, raise_if_not_found=False)
        self.assertTrue(record, f'{exercise}: no existe el xml id {xmlid}')
        return record

    def test_ex25_tag_views(self):
        list_view = self._ref('cd_practices.view_cd_practice_tag_list', 'EJERCICIO 25')
        self.assertEqual(list_view.model, 'cd.practice.tag', 'EJERCICIO 25: modelo de la vista list')
        form_view = self._ref('cd_practices.view_cd_practice_tag_form', 'EJERCICIO 25')
        self.assertEqual(form_view.model, 'cd.practice.tag', 'EJERCICIO 25: modelo de la vista form')
        action = self._ref('cd_practices.action_cd_practice_tag', 'EJERCICIO 25')
        self.assertEqual(action.res_model, 'cd.practice.tag', 'EJERCICIO 25: res_model de la acción')
        self._ref('cd_practices.menu_cd_practice_tag', 'EJERCICIO 25')

    def test_ex26_partner_fields(self):
        Partner = self.env['res.partner']
        self.assertIn(
            'practice_item_ids', Partner._fields,
            'EJERCICIO 26: falta el campo practice_item_ids en res.partner',
        )
        self.assertIn(
            'practice_item_count', Partner._fields,
            'EJERCICIO 26: falta el campo practice_item_count en res.partner',
        )
        self.assertTrue(
            hasattr(Partner, 'action_view_practice_items'),
            'EJERCICIO 26: falta el método action_view_practice_items',
        )
        partner = Partner.create({'name': 'Partner prácticas'})
        self.Item.create({'name': 'Suyo', 'owner_id': partner.id})
        self.assertEqual(
            partner.practice_item_count, 1,
            'EJERCICIO 26: practice_item_count debe contar los elementos del partner',
        )
        action = partner.action_view_practice_items()
        self.assertEqual(
            action.get('res_model'), 'cd.practice.item',
            'EJERCICIO 26: la acción debe abrir cd.practice.item',
        )
        domain = [tuple(item) for item in (action.get('domain') or [])]
        self.assertIn(
            ('owner_id', '=', partner.id), domain,
            'EJERCICIO 26: el dominio debe filtrar por owner_id',
        )

    def test_ex27_partner_view_inherit(self):
        view = self._ref(
            'cd_practices.view_res_partner_form_inherit_practice',
            'EJERCICIO 27',
        )
        arch = view.get_combined_arch()
        self.assertIn('practice_item_count', arch, 'EJERCICIO 27: añade practice_item_count')
        self.assertIn('practice_item_ids', arch, 'EJERCICIO 27: añade practice_item_ids')
        self.assertIn(
            'action_view_practice_items', arch,
            'EJERCICIO 27: añade el botón action_view_practice_items',
        )

    def test_ex28_button_and_method(self):
        draft = self.Item.create({'name': 'Borrador'})
        available = self.Item.create({'name': 'Disponible', 'state': 'available'})
        result = draft.action_mark_available()
        self.assertEqual(
            draft.state, 'available',
            'EJERCICIO 28a: action_mark_available debe pasar de draft a available',
        )
        self.assertEqual(
            available.state, 'available',
            'EJERCICIO 28a: no debe tocar los registros que no están en draft',
        )
        self.assertTrue(result, 'EJERCICIO 28a: debe devolver True')
        view = self.env.ref('cd_practices.view_cd_practice_item_form')
        arch = view.get_combined_arch()
        self.assertIn(
            'action_mark_available', arch,
            'EJERCICIO 28b: añade el botón action_mark_available en el header de la vista',
        )
        self.assertIn(
            'invisible', arch,
            "EJERCICIO 28b: el botón debe llevar invisible=\"state != 'draft'\"",
        )

    def test_ex29_server_action(self):
        action = self._ref(
            'cd_practices.action_server_reset_item_state',
            'EJERCICIO 29',
        )
        self.assertEqual(
            action.model_id.model, 'cd.practice.item',
            'EJERCICIO 29: el server action debe ser del modelo cd.practice.item',
        )
        item = self.Item.create({'name': 'Reset', 'state': 'available'})
        action.with_context(
            active_model='cd.practice.item',
            active_ids=item.ids,
        ).run()
        self.assertEqual(
            item.state, 'draft',
            'EJERCICIO 29: el código del server action debe reiniciar el estado',
        )
