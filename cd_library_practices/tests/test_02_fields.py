from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase, tagged
from odoo.tools import mute_logger


@tagged('cd_library_practice', '-standard')
class TestFields(TransactionCase):
    """Bloque 2 · Campos y decoradores (ejercicios 9 a 18)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Book = cls.env['cd.library.book']
        cls.Copy = cls.env['cd.library.copy']

    def _assert_field(self, model, field_name, exercise):
        self.assertIn(
            field_name,
            model._fields,
            f'{exercise}: falta el campo {field_name} en {model._name}',
        )

    def test_ex09_cost_with_tax(self):
        self._assert_field(self.Book, 'replacement_cost_with_tax', 'EJERCICIO 9')
        book = self.Book.create({'name': 'IVA', 'replacement_cost': 100.0})
        self.assertAlmostEqual(
            book.replacement_cost_with_tax, 121.0, places=2,
            msg='EJERCICIO 9: 100 con 21% de IVA debe ser 121',
        )
        book.replacement_cost = 200.0
        self.assertAlmostEqual(
            book.replacement_cost_with_tax, 242.0, places=2,
            msg='EJERCICIO 9: el campo almacenado debe recalcularse al cambiar el coste',
        )

    def test_ex10_cost_with_markup(self):
        self._assert_field(self.Book, 'cost_with_markup', 'EJERCICIO 10')
        book = self.Book.create({'name': 'Margen', 'replacement_cost': 100.0})
        self.assertAlmostEqual(
            book.cost_with_markup, 100.0, places=2,
            msg='EJERCICIO 10: sin library_markup en el contexto debe valer el coste',
        )
        self.assertAlmostEqual(
            book.with_context(library_markup=50).cost_with_markup, 150.0, places=2,
            msg='EJERCICIO 10: con library_markup=50 debe valer 150',
        )

    def test_ex11_related_author(self):
        self._assert_field(self.Copy, 'author_id', 'EJERCICIO 11')
        partner = self.env['res.partner'].create({'name': 'Autor'})
        book = self.Book.create({'name': 'Con autor', 'author_id': partner.id})
        copy = self.Copy.create({'name': 'EJ-01', 'book_id': book.id})
        self.assertEqual(
            copy.author_id, partner,
            'EJERCICIO 11: author_id del ejemplar debe ser el autor del libro',
        )

    def test_ex12_onchange_author(self):
        with Form(self.Book) as form:
            form.name = 'Formulario'
            form.author_id = self.env['res.partner'].create({'name': 'Ana'})
            self.assertEqual(
                form.description, 'Obra de Ana',
                'EJERCICIO 12: el onchange debe rellenar description',
            )

    def test_ex13_constrains_cost(self):
        book = self.Book.create({'name': 'Costes'})
        with self.assertRaises(ValidationError):
            book.replacement_cost = -1.0

    def test_ex14_constraint_quantity(self):
        with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'):
            self.Book.create({'name': 'Cantidad negativa', 'quantity': -1})

    def test_ex15_reference_default(self):
        self._assert_field(self.Book, 'reference', 'EJERCICIO 15')
        book = self.Book.create({'name': 'Referencia'})
        self.assertRegex(
            book.reference or '',
            r'^LIB/\d{4}$',
            'EJERCICIO 15: reference debe tener el formato LIB/AAAA',
        )

    def test_ex16_display_name(self):
        book = self.Book.create({'name': 'Display', 'quantity': 3})
        self.assertEqual(
            book.display_name, 'Display [3 ejemplares]',
            'EJERCICIO 16: display_name debe ser "{name} [{quantity} ejemplares]"',
        )

    def test_ex17_copy_override(self):
        book = self.Book.create({'name': 'Original', 'state': 'available', 'quantity': 5})
        copy = book.copy()
        self.assertEqual(copy.state, 'draft', 'EJERCICIO 17: la copia debe quedar en borrador')
        self.assertEqual(copy.quantity, 1, 'EJERCICIO 17: la copia debe tener 1 ejemplar')

    def test_ex18_active_and_order(self):
        self._assert_field(self.Book, 'active', 'EJERCICIO 18')
        cheap = self.Book.create({'name': 'Barato', 'replacement_cost': 10.0})
        expensive = self.Book.create({'name': 'Caro', 'replacement_cost': 30.0})
        middle = self.Book.create({'name': 'Medio', 'replacement_cost': 20.0})
        ids = (cheap + expensive + middle).ids
        found = self.Book.search([('id', 'in', ids)])
        self.assertEqual(
            found.mapped('name'), ['Caro', 'Medio', 'Barato'],
            "EJERCICIO 18: _order = 'replacement_cost desc, name'",
        )
        cheap.active = False
        self.assertNotIn(cheap, self.Book.search([('id', 'in', ids)]))
        self.assertIn(
            cheap,
            self.Book.with_context(active_test=False).search([('id', 'in', ids)]),
            'EJERCICIO 18: sin active_test el registro archivado debe aparecer',
        )
