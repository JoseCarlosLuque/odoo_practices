from odoo.tests import TransactionCase, tagged


@tagged('cd_vet_practice', '-standard')
class TestViews(TransactionCase):
    """Bloque 4 · Vistas y acciones XML (ejercicios 25 a 29)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Pet = cls.env['cd.vet.pet']

    def _ref(self, xmlid, exercise):
        record = self.env.ref(xmlid, raise_if_not_found=False)
        self.assertTrue(record, f'{exercise}: no existe el xml id {xmlid}')
        return record

    def test_ex25_tag_views(self):
        list_view = self._ref('cd_vet_practices.view_cd_vet_tag_list', 'EJERCICIO 25')
        self.assertEqual(list_view.model, 'cd.vet.tag', 'EJERCICIO 25: modelo de la vista list')
        form_view = self._ref('cd_vet_practices.view_cd_vet_tag_form', 'EJERCICIO 25')
        self.assertEqual(form_view.model, 'cd.vet.tag', 'EJERCICIO 25: modelo de la vista form')
        action = self._ref('cd_vet_practices.action_cd_vet_tag', 'EJERCICIO 25')
        self.assertEqual(action.res_model, 'cd.vet.tag', 'EJERCICIO 25: res_model de la acción')
        self._ref('cd_vet_practices.menu_cd_vet_tag', 'EJERCICIO 25')

    def test_ex26_partner_fields(self):
        Partner = self.env['res.partner']
        self.assertIn(
            'pet_ids', Partner._fields,
            'EJERCICIO 26: falta el campo pet_ids en res.partner',
        )
        self.assertIn(
            'pet_count', Partner._fields,
            'EJERCICIO 26: falta el campo pet_count en res.partner',
        )
        self.assertTrue(
            hasattr(Partner, 'action_view_pets'),
            'EJERCICIO 26: falta el método action_view_pets',
        )
        partner = Partner.create({'name': 'Partner veterinaria'})
        self.Pet.create({'name': 'Suya', 'owner_id': partner.id})
        self.assertEqual(
            partner.pet_count, 1,
            'EJERCICIO 26: pet_count debe contar las mascotas del partner',
        )
        action = partner.action_view_pets()
        self.assertEqual(
            action.get('res_model'), 'cd.vet.pet',
            'EJERCICIO 26: la acción debe abrir cd.vet.pet',
        )
        domain = [tuple(pet) for pet in (action.get('domain') or [])]
        self.assertIn(
            ('owner_id', '=', partner.id), domain,
            'EJERCICIO 26: el dominio debe filtrar por owner_id',
        )

    def test_ex27_partner_view_inherit(self):
        view = self._ref(
            'cd_vet_practices.view_res_partner_form_inherit_vet',
            'EJERCICIO 27',
        )
        arch = view.get_combined_arch()
        self.assertIn('pet_count', arch, 'EJERCICIO 27: añade pet_count')
        self.assertIn('pet_ids', arch, 'EJERCICIO 27: añade pet_ids')
        self.assertIn(
            'action_view_pets', arch,
            'EJERCICIO 27: añade el botón action_view_pets',
        )

    def test_ex28_button_and_method(self):
        draft = self.Pet.create({'name': 'Borrador'})
        active = self.Pet.create({'name': 'Activa', 'state': 'active'})
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
        view = self.env.ref('cd_vet_practices.view_cd_vet_pet_form')
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
            'cd_vet_practices.action_server_reset_pet_state',
            'EJERCICIO 29',
        )
        self.assertEqual(
            action.model_id.model, 'cd.vet.pet',
            'EJERCICIO 29: el server action debe ser del modelo cd.vet.pet',
        )
        pet = self.Pet.create({'name': 'Reset', 'state': 'active'})
        action.with_context(
            active_model='cd.vet.pet',
            active_ids=pet.ids,
        ).run()
        self.assertEqual(
            pet.state, 'draft',
            'EJERCICIO 29: el código del server action debe reiniciar el estado',
        )
