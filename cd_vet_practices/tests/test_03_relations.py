from odoo.tests import TransactionCase, tagged


@tagged('cd_vet_practice', '-standard')
class TestRelations(TransactionCase):
    """Bloque 3 · Relaciones y ORM avanzada (ejercicios 19 a 24)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Pet = cls.env['cd.vet.pet']
        cls.Tag = cls.env['cd.vet.tag']

    def test_ex19_add_treatments(self):
        pet = self.Pet.create({'name': 'Con tratamientos'})
        treatments = pet.exercise_19_add_treatments(['Analítica', 'Vacuna'])
        self.assertEqual(
            len(treatments), 2, 'EJERCICIO 19: debe devolver los 2 tratamientos creados',
        )
        self.assertEqual(
            set(pet.treatment_ids.mapped('name')), {'Analítica', 'Vacuna'},
            'EJERCICIO 19: Command.create debe crear los tratamientos en treatment_ids',
        )

    def test_ex20_set_and_clear_tags(self):
        pet = self.Pet.create({'name': 'Con etiquetas'})
        pet.exercise_20_set_tags(['Perro', 'Gato'])
        self.assertEqual(
            set(pet.tag_ids.mapped('name')), {'Perro', 'Gato'},
            'EJERCICIO 20a: Command.set debe crear y enlazar las etiquetas',
        )
        pet.exercise_20_set_tags(['Ave'])
        self.assertEqual(
            pet.tag_ids.mapped('name'), ['Ave'],
            'EJERCICIO 20a: set debe reemplazar las etiquetas, no acumularlas',
        )
        self.assertTrue(pet.exercise_20_clear_tags(), 'EJERCICIO 20b: debe devolver True')
        self.assertFalse(pet.tag_ids, 'EJERCICIO 20b: Command.clear debe quitar todas')

    def test_ex21_inherits_owner(self):
        self.assertIn(
            'cd.vet.owner', self.env,
            'EJERCICIO 21: falta el modelo cd.vet.owner',
        )
        owner = self.env['cd.vet.owner'].create({
            'name': 'Ana Dueña',
            'owner_code': 'D001',
        })
        self.assertTrue(owner.partner_id, 'EJERCICIO 21: _inherits debe crear el res.partner')
        self.assertEqual(owner.partner_id.name, 'Ana Dueña')
        owner.partner_id.name = 'Ana Cambiada'
        self.assertEqual(
            owner.name, 'Ana Cambiada',
            'EJERCICIO 21: los campos delegados deben sincronizarse',
        )

    def test_ex22_tag_names_inverse(self):
        self.assertIn(
            'tag_names', self.Pet._fields,
            'EJERCICIO 22: falta el campo tag_names',
        )
        tag_a = self.Tag.create({'name': 'A'})
        tag_b = self.Tag.create({'name': 'B'})
        pet = self.Pet.create({
            'name': 'Nombres',
            'tag_ids': [(6, 0, (tag_a + tag_b).ids)],
        })
        self.assertEqual(
            pet.tag_names, 'A, B',
            'EJERCICIO 22: el compute debe unir los nombres con ", "',
        )
        pet.tag_names = 'C, A'
        self.assertEqual(
            set(pet.tag_ids.mapped('name')), {'C', 'A'},
            'EJERCICIO 22: el inverse debe crear/relacionar las etiquetas indicadas',
        )

    def test_ex23_read_group(self):
        self.Pet.with_context(active_test=False).search([]).unlink()
        self.Pet.create({'name': 'D1'})
        self.Pet.create({'name': 'D2'})
        self.Pet.create({'name': 'A1', 'state': 'active'})
        result = dict(self.Pet.exercise_23_read_group_by_state())
        self.assertEqual(result.get('draft'), 2, 'EJERCICIO 23: deben contarse 2 borradores')
        self.assertEqual(result.get('active'), 1, 'EJERCICIO 23: debe contarse 1 activa')

    def test_ex24_search_fetch(self):
        self.Pet.with_context(active_test=False).search([]).unlink()
        self.Pet.create({'name': 'A', 'state': 'active', 'price': 5.0})
        self.Pet.create({'name': 'B', 'state': 'active', 'price': 15.0})
        self.Pet.create({'name': 'C', 'state': 'draft', 'price': 50.0})
        pets = self.Pet.exercise_24_search_fetch_active()
        self.assertEqual(
            pets.mapped('name'), ['B', 'A'],
            'EJERCICIO 24: search_fetch de activas ordenadas por precio desc',
        )
