from odoo.tests import TransactionCase, tagged


@tagged('cd_furniture_practice', '-standard')
class TestViews(TransactionCase):
    """Bloque 4 · Vistas y acciones XML (ejercicios 25 a 29)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['cd.furniture.product']

    def _ref(self, xmlid, exercise):
        record = self.env.ref(xmlid, raise_if_not_found=False)
        self.assertTrue(record, f'{exercise}: no existe el xml id {xmlid}')
        return record

    def test_ex25_material_views(self):
        list_view = self._ref(
            'cd_furniture_practices.view_cd_furniture_material_list', 'EJERCICIO 25',
        )
        self.assertEqual(
            list_view.model, 'cd.furniture.material', 'EJERCICIO 25: modelo de la vista list',
        )
        form_view = self._ref(
            'cd_furniture_practices.view_cd_furniture_material_form', 'EJERCICIO 25',
        )
        self.assertEqual(
            form_view.model, 'cd.furniture.material', 'EJERCICIO 25: modelo de la vista form',
        )
        action = self._ref('cd_furniture_practices.action_cd_furniture_material', 'EJERCICIO 25')
        self.assertEqual(
            action.res_model, 'cd.furniture.material', 'EJERCICIO 25: res_model de la acción',
        )
        self._ref('cd_furniture_practices.menu_cd_furniture_material', 'EJERCICIO 25')

    def test_ex26_partner_fields(self):
        Partner = self.env['res.partner']
        self.assertIn(
            'designed_product_ids', Partner._fields,
            'EJERCICIO 26: falta el campo designed_product_ids en res.partner',
        )
        self.assertIn(
            'designed_product_count', Partner._fields,
            'EJERCICIO 26: falta el campo designed_product_count en res.partner',
        )
        self.assertTrue(
            hasattr(Partner, 'action_view_designed_products'),
            'EJERCICIO 26: falta el método action_view_designed_products',
        )
        partner = Partner.create({'name': 'Partner fábrica'})
        self.Product.create({'name': 'Suyo', 'designer_id': partner.id})
        self.assertEqual(
            partner.designed_product_count, 1,
            'EJERCICIO 26: designed_product_count debe contar los muebles del partner',
        )
        action = partner.action_view_designed_products()
        self.assertEqual(
            action.get('res_model'), 'cd.furniture.product',
            'EJERCICIO 26: la acción debe abrir cd.furniture.product',
        )
        domain = [tuple(product) for product in (action.get('domain') or [])]
        self.assertIn(
            ('designer_id', '=', partner.id), domain,
            'EJERCICIO 26: el dominio debe filtrar por designer_id',
        )

    def test_ex27_partner_view_inherit(self):
        view = self._ref(
            'cd_furniture_practices.view_res_partner_form_inherit_furniture',
            'EJERCICIO 27',
        )
        arch = view.get_combined_arch()
        self.assertIn('designed_product_count', arch, 'EJERCICIO 27: añade designed_product_count')
        self.assertIn('designed_product_ids', arch, 'EJERCICIO 27: añade designed_product_ids')
        self.assertIn(
            'action_view_designed_products', arch,
            'EJERCICIO 27: añade el botón action_view_designed_products',
        )

    def test_ex28_button_and_method(self):
        draft = self.Product.create({'name': 'Borrador'})
        available = self.Product.create({'name': 'Disponible', 'state': 'available'})
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
        view = self.env.ref('cd_furniture_practices.view_cd_furniture_product_form')
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
            'cd_furniture_practices.action_server_reset_product_state',
            'EJERCICIO 29',
        )
        self.assertEqual(
            action.model_id.model, 'cd.furniture.product',
            'EJERCICIO 29: el server action debe ser del modelo cd.furniture.product',
        )
        product = self.Product.create({'name': 'Reset', 'state': 'available'})
        action.with_context(
            active_model='cd.furniture.product',
            active_ids=product.ids,
        ).run()
        self.assertEqual(
            product.state, 'draft',
            'EJERCICIO 29: el código del server action debe reiniciar el estado',
        )
