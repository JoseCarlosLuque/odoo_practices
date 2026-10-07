from odoo.tests import TransactionCase, tagged


@tagged('cd_library_practice', '-standard')
class TestOrmBasics(TransactionCase):
    """Bloque 1 · ORM básica (ejercicios 1 a 8)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Book = cls.env['cd.library.book']

    def _create_book(self, name, **vals):
        return self.Book.create({'name': name, **vals})

    def test_ex01_create_books(self):
        books = self.Book.exercise_01_create_books()
        self.assertEqual(len(books), 3, 'EJERCICIO 1: create() debe devolver 3 libros')
        by_name = {book.name: book for book in books}
        self.assertEqual(
            set(by_name),
            {'Libro A', 'Libro B', 'Libro C'},
            'EJERCICIO 1: los títulos deben ser Libro A, Libro B y Libro C',
        )
        self.assertAlmostEqual(
            by_name['Libro A'].replacement_cost, 10.0, msg='EJERCICIO 1: coste de Libro A',
        )
        self.assertAlmostEqual(
            by_name['Libro B'].replacement_cost, 20.0, msg='EJERCICIO 1: coste de Libro B',
        )
        self.assertAlmostEqual(
            by_name['Libro C'].replacement_cost, 30.0, msg='EJERCICIO 1: coste de Libro C',
        )

    def test_ex02_search_books(self):
        # Limpia datos preexistentes (p. ej. demo) para que el test sea
        # determinista; el cambio se revierte al terminar (TransactionCase).
        self.Book.with_context(active_test=False).search([]).unlink()
        self._create_book('Barato', replacement_cost=5.0)
        self._create_book('Medio', replacement_cost=10.0)
        self._create_book('Caro', replacement_cost=15.0)
        self._create_book('Muy caro', replacement_cost=20.0)
        books = self.Book.exercise_02_search_books(10.0, 2)
        self.assertEqual(
            books.mapped('name'),
            ['Muy caro', 'Caro'],
            'EJERCICIO 2: dominio coste >= 10, orden coste desc y limit 2',
        )

    def test_ex03_count_by_author(self):
        ana = self.env['res.partner'].create({'name': 'Ana'})
        bruno = self.env['res.partner'].create({'name': 'Bruno'})
        self._create_book('A1', author_id=ana.id)
        self._create_book('A2', author_id=ana.id)
        self._create_book('B1', author_id=bruno.id)
        self._create_book('Sin autor')
        self.assertEqual(
            self.Book.exercise_03_count_books_by_author(ana),
            2,
            'EJERCICIO 3: Ana debe tener 2 libros',
        )
        self.assertEqual(
            self.Book.exercise_03_count_books_by_author(bruno),
            1,
            'EJERCICIO 3: Bruno debe tener 1 libro',
        )

    def test_ex04_expensive_titles(self):
        self.Book.with_context(active_test=False).search([]).unlink()
        self._create_book('Zeta', replacement_cost=5.0)
        self._create_book('Alfa', replacement_cost=15.0)
        self._create_book('Media', replacement_cost=25.0)
        names = self.Book.exercise_04_expensive_book_titles(10.0)
        self.assertEqual(
            names,
            ['Alfa', 'Media'],
            'EJERCICIO 4: coste ESTRICTAMENTE mayor que 10 y títulos ordenados alfabéticamente',
        )

    def test_ex05_set_state(self):
        a = self._create_book('A')
        b = self._create_book('B')
        c = self._create_book('C')
        count = self.Book.exercise_05_set_state(['A', 'B'], 'available')
        self.assertEqual(count, 2, 'EJERCICIO 5: debe devolver 2 registros modificados')
        self.assertEqual(a.state, 'available', 'EJERCICIO 5: A debe estar disponible')
        self.assertEqual(b.state, 'available', 'EJERCICIO 5: B debe estar disponible')
        self.assertEqual(c.state, 'draft', 'EJERCICIO 5: C no debe haberse tocado')

    def test_ex06_delete_withdrawn(self):
        withdrawn = self._create_book('R1', state='withdrawn')
        draft = self._create_book('D1')
        deleted = self.Book.exercise_06_delete_withdrawn()
        self.assertEqual(deleted, 1, 'EJERCICIO 6: debe borrar 1 libro retirado')
        self.assertFalse(withdrawn.exists(), 'EJERCICIO 6: el retirado debe estar borrado')
        self.assertTrue(draft.exists(), 'EJERCICIO 6: el borrador no debe borrarse')

    def test_ex07_complex_domain(self):
        self._create_book('Alfa', description='contiene orm', replacement_cost=10.0)
        self._create_book('Orme', description='otra cosa', replacement_cost=12.0)
        self._create_book('Beta', description='contiene orm', replacement_cost=5.0)
        self._create_book('Gamma', description='nada', replacement_cost=50.0)
        names = self.Book.exercise_07_complex_domain('orm', 10.0)
        self.assertEqual(
            sorted(names),
            ['Alfa', 'Orme'],
            'EJERCICIO 7: (name ilike orm o description ilike orm) y coste >= 10',
        )

    def test_ex08_browse_vs_search(self):
        book = self._create_book('Existe')
        result = self.Book.exercise_08_browse_vs_search([book.id, 999999])
        self.assertEqual(result.get('found'), 1, "EJERCICIO 8: 'found' debe contar los que existen")
        self.assertEqual(
            result.get('missing'),
            [999999],
            "EJERCICIO 8: 'missing' debe contener los ids inexistentes",
        )
