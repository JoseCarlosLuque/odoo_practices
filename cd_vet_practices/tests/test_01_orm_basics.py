from odoo.tests import TransactionCase, tagged


@tagged('cd_vet_practice', '-standard')
class TestOrmBasics(TransactionCase):
    """Bloque 1 · ORM básica (ejercicios 1 a 8)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Pet = cls.env['cd.vet.pet']

    def _create_pet(self, name, **vals):
        return self.Pet.create({'name': name, **vals})

    def test_ex01_create_pets(self):
        pets = self.Pet.exercise_01_create_pets()
        self.assertEqual(len(pets), 3, 'EJERCICIO 1: create() debe devolver 3 mascotas')
        by_name = {pet.name: pet for pet in pets}
        self.assertEqual(
            set(by_name),
            {'Mascota A', 'Mascota B', 'Mascota C'},
            'EJERCICIO 1: los nombres deben ser Mascota A, Mascota B y Mascota C',
        )
        self.assertAlmostEqual(by_name['Mascota A'].price, 10.0, msg='EJERCICIO 1: precio de Mascota A')
        self.assertAlmostEqual(by_name['Mascota B'].price, 20.0, msg='EJERCICIO 1: precio de Mascota B')
        self.assertAlmostEqual(by_name['Mascota C'].price, 30.0, msg='EJERCICIO 1: precio de Mascota C')

    def test_ex02_search_pets(self):
        # Limpia datos preexistentes (p. ej. demo) para que el test sea
        # determinista; el cambio se revierte al terminar (TransactionCase).
        self.Pet.with_context(active_test=False).search([]).unlink()
        self._create_pet('Barata', price=5.0)
        self._create_pet('Media', price=10.0)
        self._create_pet('Cara', price=15.0)
        self._create_pet('Muy cara', price=20.0)
        pets = self.Pet.exercise_02_search_pets(10.0, 2)
        self.assertEqual(
            pets.mapped('name'),
            ['Muy cara', 'Cara'],
            'EJERCICIO 2: dominio precio >= 10, orden precio desc y limit 2',
        )

    def test_ex03_count_by_owner(self):
        ana = self.env['res.partner'].create({'name': 'Ana'})
        bruno = self.env['res.partner'].create({'name': 'Bruno'})
        self._create_pet('A1', owner_id=ana.id)
        self._create_pet('A2', owner_id=ana.id)
        self._create_pet('B1', owner_id=bruno.id)
        self._create_pet('Sin dueño')
        self.assertEqual(
            self.Pet.exercise_03_count_pets_by_owner(ana),
            2,
            'EJERCICIO 3: Ana debe tener 2 mascotas',
        )
        self.assertEqual(
            self.Pet.exercise_03_count_pets_by_owner(bruno),
            1,
            'EJERCICIO 3: Bruno debe tener 1 mascota',
        )

    def test_ex04_expensive_names(self):
        self.Pet.with_context(active_test=False).search([]).unlink()
        self._create_pet('Zeta', price=5.0)
        self._create_pet('Alfa', price=15.0)
        self._create_pet('Media', price=25.0)
        names = self.Pet.exercise_04_expensive_pet_names(10.0)
        self.assertEqual(
            names,
            ['Alfa', 'Media'],
            'EJERCICIO 4: precio ESTRICTAMENTE mayor que 10 y nombres ordenados alfabéticamente',
        )

    def test_ex05_set_state(self):
        a = self._create_pet('A')
        b = self._create_pet('B')
        c = self._create_pet('C')
        count = self.Pet.exercise_05_set_state(['A', 'B'], 'in_treatment')
        self.assertEqual(count, 2, 'EJERCICIO 5: debe devolver 2 registros modificados')
        self.assertEqual(a.state, 'in_treatment', 'EJERCICIO 5: A debe estar en tratamiento')
        self.assertEqual(b.state, 'in_treatment', 'EJERCICIO 5: B debe estar en tratamiento')
        self.assertEqual(c.state, 'draft', 'EJERCICIO 5: C no debe haberse tocado')

    def test_ex06_delete_archived(self):
        archived = self._create_pet('R1', state='archived')
        draft = self._create_pet('D1')
        deleted = self.Pet.exercise_06_delete_archived()
        self.assertEqual(deleted, 1, 'EJERCICIO 6: debe borrar 1 mascota dada de baja')
        self.assertFalse(archived.exists(), 'EJERCICIO 6: la dada de baja debe estar borrada')
        self.assertTrue(draft.exists(), 'EJERCICIO 6: el borrador no debe borrarse')

    def test_ex07_complex_domain(self):
        self._create_pet('Alfa', description='contiene orm', price=10.0)
        self._create_pet('Orme', description='otra cosa', price=12.0)
        self._create_pet('Beta', description='contiene orm', price=5.0)
        self._create_pet('Gamma', description='nada', price=50.0)
        names = self.Pet.exercise_07_complex_domain('orm', 10.0)
        self.assertEqual(
            sorted(names),
            ['Alfa', 'Orme'],
            'EJERCICIO 7: (name ilike orm o description ilike orm) y precio >= 10',
        )

    def test_ex08_browse_vs_search(self):
        pet = self._create_pet('Existe')
        result = self.Pet.exercise_08_browse_vs_search([pet.id, 999999])
        self.assertEqual(result.get('found'), 1, "EJERCICIO 8: 'found' debe contar los que existen")
        self.assertEqual(
            result.get('missing'),
            [999999],
            "EJERCICIO 8: 'missing' debe contener los ids inexistentes",
        )
