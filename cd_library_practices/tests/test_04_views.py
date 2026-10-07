from odoo.tests import TransactionCase, tagged


@tagged('cd_library_practice', '-standard')
class TestViews(TransactionCase):
    """Bloque 4 · Vistas y acciones XML (ejercicios 25 a 29)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Book = cls.env['cd.library.book']

    def _ref(self, xmlid, exercise):
        record = self.env.ref(xmlid, raise_if_not_found=False)
        self.assertTrue(record, f'{exercise}: no existe el xml id {xmlid}')
        return record

    def test_ex25_genre_views(self):
        list_view = self._ref('cd_library_practices.view_cd_library_genre_list', 'EJERCICIO 25')
        self.assertEqual(
            list_view.model, 'cd.library.genre', 'EJERCICIO 25: modelo de la vista list',
        )
        form_view = self._ref('cd_library_practices.view_cd_library_genre_form', 'EJERCICIO 25')
        self.assertEqual(
            form_view.model, 'cd.library.genre', 'EJERCICIO 25: modelo de la vista form',
        )
        action = self._ref('cd_library_practices.action_cd_library_genre', 'EJERCICIO 25')
        self.assertEqual(
            action.res_model, 'cd.library.genre', 'EJERCICIO 25: res_model de la acción',
        )
        self._ref('cd_library_practices.menu_cd_library_genre', 'EJERCICIO 25')

    def test_ex26_partner_fields(self):
        Partner = self.env['res.partner']
        self.assertIn(
            'authored_book_ids', Partner._fields,
            'EJERCICIO 26: falta el campo authored_book_ids en res.partner',
        )
        self.assertIn(
            'authored_book_count', Partner._fields,
            'EJERCICIO 26: falta el campo authored_book_count en res.partner',
        )
        self.assertTrue(
            hasattr(Partner, 'action_view_authored_books'),
            'EJERCICIO 26: falta el método action_view_authored_books',
        )
        partner = Partner.create({'name': 'Partner biblioteca'})
        self.Book.create({'name': 'Suyo', 'author_id': partner.id})
        self.assertEqual(
            partner.authored_book_count, 1,
            'EJERCICIO 26: authored_book_count debe contar los libros del partner',
        )
        action = partner.action_view_authored_books()
        self.assertEqual(
            action.get('res_model'), 'cd.library.book',
            'EJERCICIO 26: la acción debe abrir cd.library.book',
        )
        domain = [tuple(book) for book in (action.get('domain') or [])]
        self.assertIn(
            ('author_id', '=', partner.id), domain,
            'EJERCICIO 26: el dominio debe filtrar por author_id',
        )

    def test_ex27_partner_view_inherit(self):
        view = self._ref(
            'cd_library_practices.view_res_partner_form_inherit_library',
            'EJERCICIO 27',
        )
        arch = view.get_combined_arch()
        self.assertIn('authored_book_count', arch, 'EJERCICIO 27: añade authored_book_count')
        self.assertIn('authored_book_ids', arch, 'EJERCICIO 27: añade authored_book_ids')
        self.assertIn(
            'action_view_authored_books', arch,
            'EJERCICIO 27: añade el botón action_view_authored_books',
        )

    def test_ex28_button_and_method(self):
        draft = self.Book.create({'name': 'Borrador'})
        available = self.Book.create({'name': 'Disponible', 'state': 'available'})
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
        view = self.env.ref('cd_library_practices.view_cd_library_book_form')
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
            'cd_library_practices.action_server_reset_book_state',
            'EJERCICIO 29',
        )
        self.assertEqual(
            action.model_id.model, 'cd.library.book',
            'EJERCICIO 29: el server action debe ser del modelo cd.library.book',
        )
        book = self.Book.create({'name': 'Reset', 'state': 'available'})
        action.with_context(
            active_model='cd.library.book',
            active_ids=book.ids,
        ).run()
        self.assertEqual(
            book.state, 'draft',
            'EJERCICIO 29: el código del server action debe reiniciar el estado',
        )
