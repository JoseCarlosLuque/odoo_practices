from datetime import timedelta

from markupsafe import Markup

from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('cd_clothes_practice', '-standard')
class TestMailWizardCron(TransactionCase):
    """Bloque 6 · Mail, wizards y crons (ejercicios 33 a 35)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Order = cls.env['cd.clothes.order']
        cls.Product = cls.env['cd.clothes.product']
        cls.Wizard = cls.env['cd.clothes.order.wizard']
        cls.partner = cls.env['res.partner'].create({'name': 'Cliente'})
        cls.product = cls.Product.create({'name': 'Prenda pedible'})

    def test_ex33_mail_thread(self):
        self.assertTrue(
            hasattr(self.Order, 'message_post'),
            'EJERCICIO 33: cd.clothes.order debe heredar de mail.thread',
        )
        order = self.Order.create({
            'name': 'Pedido mail',
            'product_id': self.product.id,
            'partner_id': self.partner.id,
        })
        # create() deja un marcador interno que descarta el tracking del primer
        # write; ejecutar el precommit aquí lo limpia (detalle de Odoo 19).
        self.env.cr.precommit.run()
        message = order.message_post(body=Markup('<p>Hola</p>'))
        self.assertTrue(message.id, 'EJERCICIO 33: message_post debe crear un mensaje')
        order.state = 'ongoing'
        # En Odoo 19 los mensajes de tracking se generan en un hook de
        # precommit; en tests hay que forzarlo antes de comprobarlos.
        self.env.cr.precommit.run()
        tracked = order.message_ids.filtered(lambda m: m.tracking_value_ids)
        self.assertTrue(
            tracked,
            'EJERCICIO 33: añade tracking=True al campo state',
        )

    def test_ex34_wizard(self):
        wizard = self.Wizard.create({
            'product_id': self.product.id,
            'partner_id': self.partner.id,
            'date_start': fields.Date.today(),
            'date_end': fields.Date.today() + timedelta(days=3),
        })
        action = wizard.action_create_order()
        self.assertIsInstance(action, dict, 'EJERCICIO 34: debe devolver un dict de acción')
        self.assertEqual(
            action.get('res_model'), 'cd.clothes.order',
            'EJERCICIO 34: la acción debe abrir cd.clothes.order',
        )
        order = self.Order.browse(action.get('res_id'))
        self.assertTrue(order.exists(), 'EJERCICIO 34: el pedido debe existir')
        self.assertEqual(order.product_id, self.product, 'EJERCICIO 34: prenda del pedido')
        self.assertEqual(order.partner_id, self.partner, 'EJERCICIO 34: cliente del pedido')
        self.assertEqual(
            order.date_end, fields.Date.today() + timedelta(days=3),
            'EJERCICIO 34: fecha de entrega del pedido',
        )

    def test_ex35_cron(self):
        cron = self.env.ref(
            'cd_clothes_practices.ir_cron_cd_clothes_cancel_expired_orders',
            raise_if_not_found=False,
        )
        self.assertTrue(
            cron,
            'EJERCICIO 35: no existe el cron ir_cron_cd_clothes_cancel_expired_orders',
        )
        expired = self.Order.create({
            'name': 'Caducado',
            'product_id': self.product.id,
            'partner_id': self.partner.id,
            'state': 'ongoing',
            'date_end': fields.Date.today() - timedelta(days=1),
        })
        current = self.Order.create({
            'name': 'Vigente',
            'product_id': self.product.id,
            'partner_id': self.partner.id,
            'state': 'ongoing',
            'date_end': fields.Date.today() + timedelta(days=1),
        })
        self.Order._cron_cancel_expired_orders()
        self.assertEqual(
            expired.state, 'cancelled',
            'EJERCICIO 35: el pedido caducado debe cancelarse',
        )
        self.assertEqual(
            current.state, 'ongoing',
            'EJERCICIO 35: el pedido vigente no debe tocarse',
        )
