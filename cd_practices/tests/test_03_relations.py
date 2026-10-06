from odoo.tests import TransactionCase, tagged


@tagged('cd_practice', '-standard')
class TestRelations(TransactionCase):
    """Bloque 3 · Relaciones y ORM avanzada (ejercicios 19 a 24)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Item = cls.env['cd.practice.item']
        cls.Tag = cls.env['cd.practice.tag']

    def test_ex19_add_lines(self):
        item = self.Item.create({'name': 'Con líneas'})
        lines = item.exercise_19_add_lines(['Línea 1', 'Línea 2'])
        self.assertEqual(len(lines), 2, 'EJERCICIO 19: debe devolver las 2 líneas creadas')
        self.assertEqual(
            set(item.line_ids.mapped('name')), {'Línea 1', 'Línea 2'},
            'EJERCICIO 19: Command.create debe crear las líneas en line_ids',
        )

    def test_ex20_set_and_clear_tags(self):
        item = self.Item.create({'name': 'Con etiquetas'})
        item.exercise_20_set_tags(['Rojo', 'Azul'])
        self.assertEqual(
            set(item.tag_ids.mapped('name')), {'Rojo', 'Azul'},
            'EJERCICIO 20a: Command.set debe crear y enlazar las etiquetas',
        )
        item.exercise_20_set_tags(['Verde'])
        self.assertEqual(
            item.tag_ids.mapped('name'), ['Verde'],
            'EJERCICIO 20a: set debe reemplazar las etiquetas, no acumularlas',
        )
        self.assertTrue(item.exercise_20_clear_tags(), 'EJERCICIO 20b: debe devolver True')
        self.assertFalse(item.tag_ids, 'EJERCICIO 20b: Command.clear debe quitar todas')

    def test_ex21_inherits_member(self):
        self.assertIn(
            'cd.practice.member', self.env,
            'EJERCICIO 21: falta el modelo cd.practice.member',
        )
        member = self.env['cd.practice.member'].create({
            'name': 'Ana Miembro',
            'member_code': 'M001',
        })
        self.assertTrue(member.partner_id, 'EJERCICIO 21: _inherits debe crear el res.partner')
        self.assertEqual(member.partner_id.name, 'Ana Miembro')
        member.partner_id.name = 'Ana Cambiada'
        self.assertEqual(
            member.name, 'Ana Cambiada',
            'EJERCICIO 21: los campos delegados deben sincronizarse',
        )

    def test_ex22_tag_names_inverse(self):
        self.assertIn(
            'tag_names', self.Item._fields,
            'EJERCICIO 22: falta el campo tag_names',
        )
        tag_a = self.Tag.create({'name': 'A'})
        tag_b = self.Tag.create({'name': 'B'})
        item = self.Item.create({
            'name': 'Nombres',
            'tag_ids': [(6, 0, (tag_a + tag_b).ids)],
        })
        self.assertEqual(
            item.tag_names, 'A, B',
            'EJERCICIO 22: el compute debe unir los nombres con ", "',
        )
        item.tag_names = 'C, A'
        self.assertEqual(
            set(item.tag_ids.mapped('name')), {'C', 'A'},
            'EJERCICIO 22: el inverse debe crear/relacionar las etiquetas indicadas',
        )

    def test_ex23_read_group(self):
        self.Item.create({'name': 'D1'})
        self.Item.create({'name': 'D2'})
        self.Item.create({'name': 'A1', 'state': 'available'})
        result = dict(self.Item.exercise_23_read_group_by_state())
        self.assertEqual(result.get('draft'), 2, 'EJERCICIO 23: deben contarse 2 borradores')
        self.assertEqual(result.get('available'), 1, 'EJERCICIO 23: debe contarse 1 disponible')

    def test_ex24_search_fetch(self):
        self.Item.create({'name': 'A', 'state': 'available', 'price': 5.0})
        self.Item.create({'name': 'B', 'state': 'available', 'price': 15.0})
        self.Item.create({'name': 'C', 'state': 'draft', 'price': 50.0})
        items = self.Item.exercise_24_search_fetch_available()
        self.assertEqual(
            items.mapped('name'), ['B', 'A'],
            'EJERCICIO 24: search_fetch de disponibles ordenados por precio desc',
        )
