from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, new_test_user, tagged


@tagged('cd_furniture_practice', '-standard')
class TestSecurity(TransactionCase):
    """Bloque 5 · Seguridad (ejercicios 30 a 32)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['cd.furniture.product']

    def test_ex30_group_and_acl(self):
        group = self.env.ref(
            'cd_furniture_practices.group_cd_furniture_manager',
            raise_if_not_found=False,
        )
        self.assertTrue(
            group,
            'EJERCICIO 30: no existe el grupo group_cd_furniture_manager',
        )
        basic = new_test_user(self.env, login='furniture_basic_user')
        manager = new_test_user(
            self.env,
            login='furniture_manager_user',
            groups='base.group_user,cd_furniture_practices.group_cd_furniture_manager',
        )
        self.Product.with_user(basic).search([])
        with self.assertRaises(AccessError):
            self.Product.with_user(basic).create({'name': 'No permitido'})
        allowed = self.Product.with_user(manager).create({'name': 'Permitido'})
        self.assertTrue(allowed, 'EJERCICIO 30: el manager debe poder crear muebles')

    def test_ex31_record_rule(self):
        rule = self.env.ref(
            'cd_furniture_practices.rule_cd_furniture_product_own_records',
            raise_if_not_found=False,
        )
        self.assertTrue(
            rule,
            'EJERCICIO 31: no existe la regla rule_cd_furniture_product_own_records',
        )
        manager = new_test_user(
            self.env,
            login='furniture_rule_manager',
            groups='base.group_user,cd_furniture_practices.group_cd_furniture_manager',
        )
        own = self.Product.with_user(manager).create({
            'name': 'Propio',
            'designer_id': manager.partner_id.id,
        })
        other = self.Product.create({'name': 'Ajeno'})
        visible = self.Product.with_user(manager).search([])
        self.assertIn(
            own, visible,
            'EJERCICIO 31: el usuario debe ver sus propios muebles',
        )
        self.assertNotIn(
            other, visible,
            'EJERCICIO 31: el usuario NO debe ver muebles ajenos',
        )

    def test_ex32_has_access(self):
        self.assertTrue(
            self.Product.exercise_32_has_write_access(),
            'EJERCICIO 32: el administrador debe poder escribir',
        )
        basic = new_test_user(self.env, login='furniture_access_user')
        self.assertFalse(
            self.Product.with_user(basic).exercise_32_has_write_access(),
            'EJERCICIO 32: un usuario básico no debe poder escribir',
        )
