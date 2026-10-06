from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase, tagged
from odoo.tools import mute_logger


@tagged('cd_practice', '-standard')
class TestFields(TransactionCase):
    """Bloque 2 · Campos y decoradores (ejercicios 9 a 18)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Item = cls.env['cd.practice.item']
        cls.ItemLine = cls.env['cd.practice.item.line']

    def _assert_field(self, model, field_name, exercise):
        self.assertIn(
            field_name,
            model._fields,
            f'{exercise}: falta el campo {field_name} en {model._name}',
        )

    def test_ex09_price_with_tax(self):
        self._assert_field(self.Item, 'price_with_tax', 'EJERCICIO 9')
        item = self.Item.create({'name': 'IVA', 'price': 100.0})
        self.assertAlmostEqual(
            item.price_with_tax, 121.0, places=2,
            msg='EJERCICIO 9: 100 con 21% de IVA debe ser 121',
        )
        item.price = 200.0
        self.assertAlmostEqual(
            item.price_with_tax, 242.0, places=2,
            msg='EJERCICIO 9: el campo almacenado debe recalcularse al cambiar el precio',
        )

    def test_ex10_price_with_markup(self):
        self._assert_field(self.Item, 'price_with_markup', 'EJERCICIO 10')
        item = self.Item.create({'name': 'Margen', 'price': 100.0})
        self.assertAlmostEqual(
            item.price_with_markup, 100.0, places=2,
            msg='EJERCICIO 10: sin practice_markup en el contexto debe valer price',
        )
        self.assertAlmostEqual(
            item.with_context(practice_markup=50).price_with_markup, 150.0, places=2,
            msg='EJERCICIO 10: con practice_markup=50 debe valer 150',
        )

    def test_ex11_related_owner(self):
        self._assert_field(self.ItemLine, 'owner_id', 'EJERCICIO 11')
        partner = self.env['res.partner'].create({'name': 'Dueño'})
        item = self.Item.create({'name': 'Con dueño', 'owner_id': partner.id})
        line = self.ItemLine.create({'name': 'Línea', 'item_id': item.id})
        self.assertEqual(
            line.owner_id, partner,
            'EJERCICIO 11: owner_id de la línea debe ser el propietario del elemento',
        )

    def test_ex12_onchange_owner(self):
        with Form(self.Item) as form:
            form.name = 'Formulario'
            form.owner_id = self.env['res.partner'].create({'name': 'Ana'})
            self.assertEqual(
                form.description, 'Propiedad de Ana',
                'EJERCICIO 12: el onchange debe rellenar description',
            )

    def test_ex13_constrains_price(self):
        item = self.Item.create({'name': 'Precios'})
        with self.assertRaises(ValidationError):
            item.price = -1.0

    def test_ex14_constraint_quantity(self):
        with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'):
            self.Item.create({'name': 'Cantidad negativa', 'quantity': -1})

    def test_ex15_reference_default(self):
        self._assert_field(self.Item, 'reference', 'EJERCICIO 15')
        item = self.Item.create({'name': 'Referencia'})
        self.assertRegex(
            item.reference or '',
            r'^ITEM/\d{4}$',
            'EJERCICIO 15: reference debe tener el formato ITEM/AAAA',
        )

    def test_ex16_display_name(self):
        item = self.Item.create({'name': 'Display', 'quantity': 3})
        self.assertEqual(
            item.display_name, 'Display [3 uds]',
            'EJERCICIO 16: display_name debe ser "{name} [{quantity} uds]"',
        )

    def test_ex17_copy_override(self):
        item = self.Item.create({'name': 'Original', 'state': 'available', 'quantity': 5})
        copy = item.copy()
        self.assertEqual(copy.state, 'draft', 'EJERCICIO 17: la copia debe quedar en borrador')
        self.assertEqual(copy.quantity, 1, 'EJERCICIO 17: la copia debe tener cantidad 1')

    def test_ex18_active_and_order(self):
        self._assert_field(self.Item, 'active', 'EJERCICIO 18')
        cheap = self.Item.create({'name': 'Barato', 'price': 10.0})
        expensive = self.Item.create({'name': 'Caro', 'price': 30.0})
        middle = self.Item.create({'name': 'Medio', 'price': 20.0})
        ids = (cheap + expensive + middle).ids
        found = self.Item.search([('id', 'in', ids)])
        self.assertEqual(
            found.mapped('name'), ['Caro', 'Medio', 'Barato'],
            "EJERCICIO 18: _order = 'price desc, name'",
        )
        cheap.active = False
        self.assertNotIn(cheap, self.Item.search([('id', 'in', ids)]))
        self.assertIn(
            cheap,
            self.Item.with_context(active_test=False).search([('id', 'in', ids)]),
            'EJERCICIO 18: sin active_test el registro archivado debe aparecer',
        )
