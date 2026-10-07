from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase, tagged
from odoo.tools import mute_logger


@tagged('cd_vet_practice', '-standard')
class TestFields(TransactionCase):
    """Bloque 2 · Campos y decoradores (ejercicios 9 a 18)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Pet = cls.env['cd.vet.pet']
        cls.Treatment = cls.env['cd.vet.treatment']

    def _assert_field(self, model, field_name, exercise):
        self.assertIn(
            field_name,
            model._fields,
            f'{exercise}: falta el campo {field_name} en {model._name}',
        )

    def test_ex09_price_with_tax(self):
        self._assert_field(self.Pet, 'price_with_tax', 'EJERCICIO 9')
        pet = self.Pet.create({'name': 'IVA', 'price': 100.0})
        self.assertAlmostEqual(
            pet.price_with_tax, 121.0, places=2,
            msg='EJERCICIO 9: 100 con 21% de IVA debe ser 121',
        )
        pet.price = 200.0
        self.assertAlmostEqual(
            pet.price_with_tax, 242.0, places=2,
            msg='EJERCICIO 9: el campo almacenado debe recalcularse al cambiar el precio',
        )

    def test_ex10_price_with_markup(self):
        self._assert_field(self.Pet, 'price_with_markup', 'EJERCICIO 10')
        pet = self.Pet.create({'name': 'Margen', 'price': 100.0})
        self.assertAlmostEqual(
            pet.price_with_markup, 100.0, places=2,
            msg='EJERCICIO 10: sin vet_markup en el contexto debe valer price',
        )
        self.assertAlmostEqual(
            pet.with_context(vet_markup=50).price_with_markup, 150.0, places=2,
            msg='EJERCICIO 10: con vet_markup=50 debe valer 150',
        )

    def test_ex11_related_owner(self):
        self._assert_field(self.Treatment, 'owner_id', 'EJERCICIO 11')
        partner = self.env['res.partner'].create({'name': 'Dueño'})
        pet = self.Pet.create({'name': 'Con dueño', 'owner_id': partner.id})
        treatment = self.Treatment.create({'name': 'Tratamiento', 'pet_id': pet.id})
        self.assertEqual(
            treatment.owner_id, partner,
            'EJERCICIO 11: owner_id del tratamiento debe ser el dueño de la mascota',
        )

    def test_ex12_onchange_owner(self):
        with Form(self.Pet) as form:
            form.name = 'Formulario'
            form.owner_id = self.env['res.partner'].create({'name': 'Ana'})
            self.assertEqual(
                form.description, 'Mascota de Ana',
                'EJERCICIO 12: el onchange debe rellenar description',
            )

    def test_ex13_constrains_price(self):
        pet = self.Pet.create({'name': 'Precios'})
        with self.assertRaises(ValidationError):
            pet.price = -1.0

    def test_ex14_constraint_quantity(self):
        with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'):
            self.Pet.create({'name': 'Sesiones negativas', 'quantity': -1})

    def test_ex15_reference_default(self):
        self._assert_field(self.Pet, 'reference', 'EJERCICIO 15')
        pet = self.Pet.create({'name': 'Referencia'})
        self.assertRegex(
            pet.reference or '',
            r'^VET/\d{4}$',
            'EJERCICIO 15: reference debe tener el formato VET/AAAA',
        )

    def test_ex16_display_name(self):
        pet = self.Pet.create({'name': 'Display', 'quantity': 3})
        self.assertEqual(
            pet.display_name, 'Display [3 sesiones]',
            'EJERCICIO 16: display_name debe ser "{name} [{quantity} sesiones]"',
        )

    def test_ex17_copy_override(self):
        pet = self.Pet.create({'name': 'Original', 'state': 'active', 'quantity': 5})
        copy = pet.copy()
        self.assertEqual(copy.state, 'draft', 'EJERCICIO 17: la copia debe quedar en borrador')
        self.assertEqual(copy.quantity, 1, 'EJERCICIO 17: la copia debe tener 1 sesión')

    def test_ex18_active_and_order(self):
        self._assert_field(self.Pet, 'active', 'EJERCICIO 18')
        cheap = self.Pet.create({'name': 'Barata', 'price': 10.0})
        expensive = self.Pet.create({'name': 'Cara', 'price': 30.0})
        middle = self.Pet.create({'name': 'Media', 'price': 20.0})
        ids = (cheap + expensive + middle).ids
        found = self.Pet.search([('id', 'in', ids)])
        self.assertEqual(
            found.mapped('name'), ['Cara', 'Media', 'Barata'],
            "EJERCICIO 18: _order = 'price desc, name'",
        )
        cheap.active = False
        self.assertNotIn(cheap, self.Pet.search([('id', 'in', ids)]))
        self.assertIn(
            cheap,
            self.Pet.with_context(active_test=False).search([('id', 'in', ids)]),
            'EJERCICIO 18: sin active_test el registro archivado debe aparecer',
        )
