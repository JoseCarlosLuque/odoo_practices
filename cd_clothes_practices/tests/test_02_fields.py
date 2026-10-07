from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase, tagged
from odoo.tools import mute_logger


@tagged('cd_clothes_practice', '-standard')
class TestFields(TransactionCase):
    """Bloque 2 · Campos y decoradores (ejercicios 9 a 18)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['cd.clothes.product']
        cls.Variant = cls.env['cd.clothes.variant']

    def _assert_field(self, model, field_name, exercise):
        self.assertIn(
            field_name,
            model._fields,
            f'{exercise}: falta el campo {field_name} en {model._name}',
        )

    def test_ex09_price_with_tax(self):
        self._assert_field(self.Product, 'price_with_tax', 'EJERCICIO 9')
        product = self.Product.create({'name': 'IVA', 'price': 100.0})
        self.assertAlmostEqual(
            product.price_with_tax, 121.0, places=2,
            msg='EJERCICIO 9: 100 con 21% de IVA debe ser 121',
        )
        product.price = 200.0
        self.assertAlmostEqual(
            product.price_with_tax, 242.0, places=2,
            msg='EJERCICIO 9: el campo almacenado debe recalcularse al cambiar el precio',
        )

    def test_ex10_price_with_markup(self):
        self._assert_field(self.Product, 'price_with_markup', 'EJERCICIO 10')
        product = self.Product.create({'name': 'Margen', 'price': 100.0})
        self.assertAlmostEqual(
            product.price_with_markup, 100.0, places=2,
            msg='EJERCICIO 10: sin clothes_markup en el contexto debe valer price',
        )
        self.assertAlmostEqual(
            product.with_context(clothes_markup=50).price_with_markup, 150.0, places=2,
            msg='EJERCICIO 10: con clothes_markup=50 debe valer 150',
        )

    def test_ex11_related_supplier(self):
        self._assert_field(self.Variant, 'supplier_id', 'EJERCICIO 11')
        partner = self.env['res.partner'].create({'name': 'Proveedor'})
        product = self.Product.create({'name': 'Con proveedor', 'supplier_id': partner.id})
        variant = self.Variant.create({'name': 'Talla M', 'product_id': product.id})
        self.assertEqual(
            variant.supplier_id, partner,
            'EJERCICIO 11: supplier_id de la variante debe ser el proveedor de la prenda',
        )

    def test_ex12_onchange_supplier(self):
        with Form(self.Product) as form:
            form.name = 'Formulario'
            form.supplier_id = self.env['res.partner'].create({'name': 'Ana'})
            self.assertEqual(
                form.description, 'Prenda de Ana',
                'EJERCICIO 12: el onchange debe rellenar description',
            )

    def test_ex13_constrains_price(self):
        product = self.Product.create({'name': 'Precios'})
        with self.assertRaises(ValidationError):
            product.price = -1.0

    def test_ex14_constraint_quantity(self):
        with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'):
            self.Product.create({'name': 'Stock negativo', 'quantity': -1})

    def test_ex15_reference_default(self):
        self._assert_field(self.Product, 'reference', 'EJERCICIO 15')
        product = self.Product.create({'name': 'Referencia'})
        self.assertRegex(
            product.reference or '',
            r'^ROP/\d{4}$',
            'EJERCICIO 15: reference debe tener el formato ROP/AAAA',
        )

    def test_ex16_display_name(self):
        product = self.Product.create({'name': 'Display', 'quantity': 3})
        self.assertEqual(
            product.display_name, 'Display [3 uds]',
            'EJERCICIO 16: display_name debe ser "{name} [{quantity} uds]"',
        )

    def test_ex17_copy_override(self):
        product = self.Product.create({'name': 'Original', 'state': 'available', 'quantity': 5})
        copy = product.copy()
        self.assertEqual(copy.state, 'draft', 'EJERCICIO 17: la copia debe quedar en borrador')
        self.assertEqual(copy.quantity, 1, 'EJERCICIO 17: la copia debe tener 1 unidad')

    def test_ex18_active_and_order(self):
        self._assert_field(self.Product, 'active', 'EJERCICIO 18')
        cheap = self.Product.create({'name': 'Barata', 'price': 10.0})
        expensive = self.Product.create({'name': 'Cara', 'price': 30.0})
        middle = self.Product.create({'name': 'Media', 'price': 20.0})
        ids = (cheap + expensive + middle).ids
        found = self.Product.search([('id', 'in', ids)])
        self.assertEqual(
            found.mapped('name'), ['Cara', 'Media', 'Barata'],
            "EJERCICIO 18: _order = 'price desc, name'",
        )
        cheap.active = False
        self.assertNotIn(cheap, self.Product.search([('id', 'in', ids)]))
        self.assertIn(
            cheap,
            self.Product.with_context(active_test=False).search([('id', 'in', ids)]),
            'EJERCICIO 18: sin active_test el registro archivado debe aparecer',
        )
