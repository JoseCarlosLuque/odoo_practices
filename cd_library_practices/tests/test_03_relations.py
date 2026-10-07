from odoo.tests import TransactionCase, tagged


@tagged('cd_library_practice', '-standard')
class TestRelations(TransactionCase):
    """Bloque 3 · Relaciones y ORM avanzada (ejercicios 19 a 24)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Book = cls.env['cd.library.book']
        cls.Genre = cls.env['cd.library.genre']

    def test_ex19_add_copies(self):
        book = self.Book.create({'name': 'Con ejemplares'})
        copies = book.exercise_19_add_copies(['EJ-01', 'EJ-02'])
        self.assertEqual(len(copies), 2, 'EJERCICIO 19: debe devolver los 2 ejemplares creados')
        self.assertEqual(
            set(book.copy_ids.mapped('name')), {'EJ-01', 'EJ-02'},
            'EJERCICIO 19: Command.create debe crear los ejemplares en copy_ids',
        )

    def test_ex20_set_and_clear_genres(self):
        book = self.Book.create({'name': 'Con géneros'})
        book.exercise_20_set_genres(['Aventura', 'Misterio'])
        self.assertEqual(
            set(book.genre_ids.mapped('name')), {'Aventura', 'Misterio'},
            'EJERCICIO 20a: Command.set debe crear y enlazar los géneros',
        )
        book.exercise_20_set_genres(['Terror'])
        self.assertEqual(
            book.genre_ids.mapped('name'), ['Terror'],
            'EJERCICIO 20a: set debe reemplazar los géneros, no acumularlos',
        )
        self.assertTrue(book.exercise_20_clear_genres(), 'EJERCICIO 20b: debe devolver True')
        self.assertFalse(book.genre_ids, 'EJERCICIO 20b: Command.clear debe quitar todos')

    def test_ex21_inherits_member(self):
        self.assertIn(
            'cd.library.member', self.env,
            'EJERCICIO 21: falta el modelo cd.library.member',
        )
        member = self.env['cd.library.member'].create({
            'name': 'Ana Socia',
            'member_code': 'M001',
        })
        self.assertTrue(member.partner_id, 'EJERCICIO 21: _inherits debe crear el res.partner')
        self.assertEqual(member.partner_id.name, 'Ana Socia')
        member.partner_id.name = 'Ana Cambiada'
        self.assertEqual(
            member.name, 'Ana Cambiada',
            'EJERCICIO 21: los campos delegados deben sincronizarse',
        )

    def test_ex22_genre_names_inverse(self):
        self.assertIn(
            'genre_names', self.Book._fields,
            'EJERCICIO 22: falta el campo genre_names',
        )
        genre_a = self.Genre.create({'name': 'A'})
        genre_b = self.Genre.create({'name': 'B'})
        book = self.Book.create({
            'name': 'Nombres',
            'genre_ids': [(6, 0, (genre_a + genre_b).ids)],
        })
        self.assertEqual(
            book.genre_names, 'A, B',
            'EJERCICIO 22: el compute debe unir los nombres con ", "',
        )
        book.genre_names = 'C, A'
        self.assertEqual(
            set(book.genre_ids.mapped('name')), {'C', 'A'},
            'EJERCICIO 22: el inverse debe crear/relacionar los géneros indicados',
        )

    def test_ex23_read_group(self):
        self.Book.with_context(active_test=False).search([]).unlink()
        self.Book.create({'name': 'D1'})
        self.Book.create({'name': 'D2'})
        self.Book.create({'name': 'A1', 'state': 'available'})
        result = dict(self.Book.exercise_23_read_group_by_state())
        self.assertEqual(result.get('draft'), 2, 'EJERCICIO 23: deben contarse 2 borradores')
        self.assertEqual(result.get('available'), 1, 'EJERCICIO 23: debe contarse 1 disponible')

    def test_ex24_search_fetch(self):
        self.Book.with_context(active_test=False).search([]).unlink()
        self.Book.create({'name': 'A', 'state': 'available', 'replacement_cost': 5.0})
        self.Book.create({'name': 'B', 'state': 'available', 'replacement_cost': 15.0})
        self.Book.create({'name': 'C', 'state': 'draft', 'replacement_cost': 50.0})
        books = self.Book.exercise_24_search_fetch_available()
        self.assertEqual(
            books.mapped('name'), ['B', 'A'],
            'EJERCICIO 24: search_fetch de disponibles ordenados por coste desc',
        )
