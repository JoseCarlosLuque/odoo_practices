from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, new_test_user, tagged


@tagged('cd_vet_practice', '-standard')
class TestSecurity(TransactionCase):
    """Bloque 5 · Seguridad (ejercicios 30 a 32)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Pet = cls.env['cd.vet.pet']

    def test_ex30_group_and_acl(self):
        group = self.env.ref(
            'cd_vet_practices.group_cd_vet_manager',
            raise_if_not_found=False,
        )
        self.assertTrue(
            group,
            'EJERCICIO 30: no existe el grupo group_cd_vet_manager',
        )
        basic = new_test_user(self.env, login='vet_basic_user')
        manager = new_test_user(
            self.env,
            login='vet_manager_user',
            groups='base.group_user,cd_vet_practices.group_cd_vet_manager',
        )
        self.Pet.with_user(basic).search([])
        with self.assertRaises(AccessError):
            self.Pet.with_user(basic).create({'name': 'No permitido'})
        allowed = self.Pet.with_user(manager).create({'name': 'Permitido'})
        self.assertTrue(allowed, 'EJERCICIO 30: el manager debe poder crear mascotas')

    def test_ex31_record_rule(self):
        rule = self.env.ref(
            'cd_vet_practices.rule_cd_vet_pet_own_records',
            raise_if_not_found=False,
        )
        self.assertTrue(
            rule,
            'EJERCICIO 31: no existe la regla rule_cd_vet_pet_own_records',
        )
        manager = new_test_user(
            self.env,
            login='vet_rule_manager',
            groups='base.group_user,cd_vet_practices.group_cd_vet_manager',
        )
        own = self.Pet.with_user(manager).create({
            'name': 'Propia',
            'owner_id': manager.partner_id.id,
        })
        other = self.Pet.create({'name': 'Ajena'})
        visible = self.Pet.with_user(manager).search([])
        self.assertIn(
            own, visible,
            'EJERCICIO 31: el usuario debe ver sus propias mascotas',
        )
        self.assertNotIn(
            other, visible,
            'EJERCICIO 31: el usuario NO debe ver mascotas ajenas',
        )

    def test_ex32_has_access(self):
        self.assertTrue(
            self.Pet.exercise_32_has_write_access(),
            'EJERCICIO 32: el administrador debe poder escribir',
        )
        basic = new_test_user(self.env, login='vet_access_user')
        self.assertFalse(
            self.Pet.with_user(basic).exercise_32_has_write_access(),
            'EJERCICIO 32: un usuario básico no debe poder escribir',
        )
