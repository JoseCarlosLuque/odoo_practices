from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase, tagged
from odoo.tools import mute_logger


@tagged('cd_gym_practice', '-standard')
class TestFields(TransactionCase):
    """Bloque 2 · Campos y decoradores (ejercicios 9 a 18)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Membership = cls.env['cd.gym.membership']
        cls.Line = cls.env['cd.gym.membership.line']

    def _assert_field(self, model, field_name, exercise):
        self.assertIn(
            field_name,
            model._fields,
            f'{exercise}: falta el campo {field_name} en {model._name}',
        )

    def test_ex09_price_with_tax(self):
        self._assert_field(self.Membership, 'price_with_tax', 'EJERCICIO 9')
        membership = self.Membership.create({'name': 'IVA', 'price': 100.0})
        self.assertAlmostEqual(
            membership.price_with_tax, 121.0, places=2,
            msg='EJERCICIO 9: 100 con 21% de IVA debe ser 121',
        )
        membership.price = 200.0
        self.assertAlmostEqual(
            membership.price_with_tax, 242.0, places=2,
            msg='EJERCICIO 9: el campo almacenado debe recalcularse al cambiar el precio',
        )

    def test_ex10_price_with_markup(self):
        self._assert_field(self.Membership, 'price_with_markup', 'EJERCICIO 10')
        membership = self.Membership.create({'name': 'Margen', 'price': 100.0})
        self.assertAlmostEqual(
            membership.price_with_markup, 100.0, places=2,
            msg='EJERCICIO 10: sin gym_markup en el contexto debe valer price',
        )
        self.assertAlmostEqual(
            membership.with_context(gym_markup=50).price_with_markup, 150.0, places=2,
            msg='EJERCICIO 10: con gym_markup=50 debe valer 150',
        )

    def test_ex11_related_partner(self):
        self._assert_field(self.Line, 'partner_id', 'EJERCICIO 11')
        partner = self.env['res.partner'].create({'name': 'Socio'})
        membership = self.Membership.create({'name': 'Con socio', 'partner_id': partner.id})
        line = self.Line.create({'name': 'Servicio', 'membership_id': membership.id})
        self.assertEqual(
            line.partner_id, partner,
            'EJERCICIO 11: partner_id del servicio debe ser el socio de la cuota',
        )

    def test_ex12_onchange_partner(self):
        with Form(self.Membership) as form:
            form.name = 'Formulario'
            form.partner_id = self.env['res.partner'].create({'name': 'Ana'})
            self.assertEqual(
                form.description, 'Cuota de Ana',
                'EJERCICIO 12: el onchange debe rellenar description',
            )

    def test_ex13_constrains_price(self):
        membership = self.Membership.create({'name': 'Precios'})
        with self.assertRaises(ValidationError):
            membership.price = -1.0

    def test_ex14_constraint_quantity(self):
        with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'):
            self.Membership.create({'name': 'Sesiones negativas', 'quantity': -1})

    def test_ex15_reference_default(self):
        self._assert_field(self.Membership, 'reference', 'EJERCICIO 15')
        membership = self.Membership.create({'name': 'Referencia'})
        self.assertRegex(
            membership.reference or '',
            r'^GYM/\d{4}$',
            'EJERCICIO 15: reference debe tener el formato GYM/AAAA',
        )

    def test_ex16_display_name(self):
        membership = self.Membership.create({'name': 'Display', 'quantity': 3})
        self.assertEqual(
            membership.display_name, 'Display [3 sesiones]',
            'EJERCICIO 16: display_name debe ser "{name} [{quantity} sesiones]"',
        )

    def test_ex17_copy_override(self):
        membership = self.Membership.create({'name': 'Original', 'state': 'active', 'quantity': 5})
        copy = membership.copy()
        self.assertEqual(copy.state, 'draft', 'EJERCICIO 17: la copia debe quedar en borrador')
        self.assertEqual(copy.quantity, 1, 'EJERCICIO 17: la copia debe tener 1 sesión')

    def test_ex18_active_and_order(self):
        self._assert_field(self.Membership, 'active', 'EJERCICIO 18')
        cheap = self.Membership.create({'name': 'Barata', 'price': 10.0})
        expensive = self.Membership.create({'name': 'Cara', 'price': 30.0})
        middle = self.Membership.create({'name': 'Media', 'price': 20.0})
        ids = (cheap + expensive + middle).ids
        found = self.Membership.search([('id', 'in', ids)])
        self.assertEqual(
            found.mapped('name'), ['Cara', 'Media', 'Barata'],
            "EJERCICIO 18: _order = 'price desc, name'",
        )
        cheap.active = False
        self.assertNotIn(cheap, self.Membership.search([('id', 'in', ids)]))
        self.assertIn(
            cheap,
            self.Membership.with_context(active_test=False).search([('id', 'in', ids)]),
            'EJERCICIO 18: sin active_test el registro archivado debe aparecer',
        )
