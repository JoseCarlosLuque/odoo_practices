from odoo.tests import TransactionCase, tagged


@tagged('cd_clothes_practice', '-standard')
class TestViews(TransactionCase):
    """Bloque 4 · Vistas y acciones XML (ejercicios 25 a 29)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['cd.clothes.product']

    def _ref(self, xmlid, exercise):
        record = self.env.ref(xmlid, raise_if_not_found=False)
        self.assertTrue(record, f'{exercise}: no existe el xml id {xmlid}')
        return record

    def test_ex25_category_views(self):
        list_view = self._ref('cd_clothes_practices.view_cd_clothes_category_list', 'EJERCICIO 25')
        self.assertEqual(
            list_view.model, 'cd.clothes.category', 'EJERCICIO 25: modelo de la vista list',
        )
        form_view = self._ref('cd_clothes_practices.view_cd_clothes_category_form', 'EJERCICIO 25')
        self.assertEqual(
            form_view.model, 'cd.clothes.category', 'EJERCICIO 25: modelo de la vista form',
        )
        action = self._ref('cd_clothes_practices.action_cd_clothes_category', 'EJERCICIO 25')
        self.assertEqual(
            action.res_model, 'cd.clothes.category', 'EJERCICIO 25: res_model de la acción',
        )
        self._ref('cd_clothes_practices.menu_cd_clothes_category', 'EJERCICIO 25')

    def test_ex26_partner_fields(self):
        Partner = self.env['res.partner']
        self.assertIn(
            'product_ids', Partner._fields,
            'EJERCICIO 26: falta el campo product_ids en res.partner',
        )
        self.assertIn(
            'product_count', Partner._fields,
            'EJERCICIO 26: falta el campo product_count en res.partner',
        )
        self.assertTrue(
            hasattr(Partner, 'action_view_products'),
            'EJERCICIO 26: falta el método action_view_products',
        )
        partner = Partner.create({'name': 'Partner tienda'})
        self.Product.create({'name': 'Suya', 'supplier_id': partner.id})
        self.assertEqual(
            partner.product_count, 1,
            'EJERCICIO 26: product_count debe contar las prendas del partner',
        )
        action = partner.action_view_products()
        self.assertEqual(
            action.get('res_model'), 'cd.clothes.product',
            'EJERCICIO 26: la acción debe abrir cd.clothes.product',
        )
        domain = [tuple(product) for product in (action.get('domain') or [])]
        self.assertIn(
            ('supplier_id', '=', partner.id), domain,
            'EJERCICIO 26: el dominio debe filtrar por supplier_id',
        )

    def test_ex27_partner_view_inherit(self):
        view = self._ref(
            'cd_clothes_practices.view_res_partner_form_inherit_clothes',
            'EJERCICIO 27',
        )
        arch = view.get_combined_arch()
        self.assertIn('product_count', arch, 'EJERCICIO 27: añade product_count')
        self.assertIn('product_ids', arch, 'EJERCICIO 27: añade product_ids')
        self.assertIn(
            'action_view_products', arch,
            'EJERCICIO 27: añade el botón action_view_products',
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
        view = self.env.ref('cd_clothes_practices.view_cd_clothes_product_form')
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
            'cd_clothes_practices.action_server_reset_product_state',
            'EJERCICIO 29',
        )
        self.assertEqual(
            action.model_id.model, 'cd.clothes.product',
            'EJERCICIO 29: el server action debe ser del modelo cd.clothes.product',
        )
        product = self.Product.create({'name': 'Reset', 'state': 'available'})
        action.with_context(
            active_model='cd.clothes.product',
            active_ids=product.ids,
        ).run()
        self.assertEqual(
            product.state, 'draft',
            'EJERCICIO 29: el código del server action debe reiniciar el estado',
        )
