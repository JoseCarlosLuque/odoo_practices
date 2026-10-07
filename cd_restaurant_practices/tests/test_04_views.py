from odoo.tests import TransactionCase, tagged


@tagged('cd_restaurant_practice', '-standard')
class TestViews(TransactionCase):
    """Bloque 4 · Vistas y acciones XML (ejercicios 25 a 29)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Dish = cls.env['cd.restaurant.dish']

    def _ref(self, xmlid, exercise):
        record = self.env.ref(xmlid, raise_if_not_found=False)
        self.assertTrue(record, f'{exercise}: no existe el xml id {xmlid}')
        return record

    def test_ex25_allergen_views(self):
        list_view = self._ref(
            'cd_restaurant_practices.view_cd_restaurant_allergen_list', 'EJERCICIO 25',
        )
        self.assertEqual(
            list_view.model, 'cd.restaurant.allergen', 'EJERCICIO 25: modelo de la vista list',
        )
        form_view = self._ref(
            'cd_restaurant_practices.view_cd_restaurant_allergen_form', 'EJERCICIO 25',
        )
        self.assertEqual(
            form_view.model, 'cd.restaurant.allergen', 'EJERCICIO 25: modelo de la vista form',
        )
        action = self._ref('cd_restaurant_practices.action_cd_restaurant_allergen', 'EJERCICIO 25')
        self.assertEqual(
            action.res_model, 'cd.restaurant.allergen', 'EJERCICIO 25: res_model de la acción',
        )
        self._ref('cd_restaurant_practices.menu_cd_restaurant_allergen', 'EJERCICIO 25')

    def test_ex26_partner_fields(self):
        Partner = self.env['res.partner']
        self.assertIn(
            'dish_ids', Partner._fields,
            'EJERCICIO 26: falta el campo dish_ids en res.partner',
        )
        self.assertIn(
            'dish_count', Partner._fields,
            'EJERCICIO 26: falta el campo dish_count en res.partner',
        )
        self.assertTrue(
            hasattr(Partner, 'action_view_dishes'),
            'EJERCICIO 26: falta el método action_view_dishes',
        )
        partner = Partner.create({'name': 'Partner restaurante'})
        self.Dish.create({'name': 'Suyo', 'chef_id': partner.id})
        self.assertEqual(
            partner.dish_count, 1,
            'EJERCICIO 26: dish_count debe contar los platos del partner',
        )
        action = partner.action_view_dishes()
        self.assertEqual(
            action.get('res_model'), 'cd.restaurant.dish',
            'EJERCICIO 26: la acción debe abrir cd.restaurant.dish',
        )
        domain = [tuple(dish) for dish in (action.get('domain') or [])]
        self.assertIn(
            ('chef_id', '=', partner.id), domain,
            'EJERCICIO 26: el dominio debe filtrar por chef_id',
        )

    def test_ex27_partner_view_inherit(self):
        view = self._ref(
            'cd_restaurant_practices.view_res_partner_form_inherit_restaurant',
            'EJERCICIO 27',
        )
        arch = view.get_combined_arch()
        self.assertIn('dish_count', arch, 'EJERCICIO 27: añade dish_count')
        self.assertIn('dish_ids', arch, 'EJERCICIO 27: añade dish_ids')
        self.assertIn(
            'action_view_dishes', arch,
            'EJERCICIO 27: añade el botón action_view_dishes',
        )

    def test_ex28_button_and_method(self):
        draft = self.Dish.create({'name': 'Borrador'})
        available = self.Dish.create({'name': 'Disponible', 'state': 'available'})
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
        view = self.env.ref('cd_restaurant_practices.view_cd_restaurant_dish_form')
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
            'cd_restaurant_practices.action_server_reset_dish_state',
            'EJERCICIO 29',
        )
        self.assertEqual(
            action.model_id.model, 'cd.restaurant.dish',
            'EJERCICIO 29: el server action debe ser del modelo cd.restaurant.dish',
        )
        dish = self.Dish.create({'name': 'Reset', 'state': 'available'})
        action.with_context(
            active_model='cd.restaurant.dish',
            active_ids=dish.ids,
        ).run()
        self.assertEqual(
            dish.state, 'draft',
            'EJERCICIO 29: el código del server action debe reiniciar el estado',
        )
