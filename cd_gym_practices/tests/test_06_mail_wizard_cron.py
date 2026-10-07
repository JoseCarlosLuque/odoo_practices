from datetime import timedelta

from markupsafe import Markup

from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('cd_gym_practice', '-standard')
class TestMailWizardCron(TransactionCase):
    """Bloque 6 · Mail, wizards y crons (ejercicios 33 a 35)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Booking = cls.env['cd.gym.booking']
        cls.Membership = cls.env['cd.gym.membership']
        cls.Wizard = cls.env['cd.gym.booking.wizard']
        cls.partner = cls.env['res.partner'].create({'name': 'Socio'})
        cls.membership = cls.Membership.create({'name': 'Cuota reservable'})

    def test_ex33_mail_thread(self):
        self.assertTrue(
            hasattr(self.Booking, 'message_post'),
            'EJERCICIO 33: cd.gym.booking debe heredar de mail.thread',
        )
        booking = self.Booking.create({
            'name': 'Reserva mail',
            'membership_id': self.membership.id,
            'partner_id': self.partner.id,
        })
        # create() deja un marcador interno que descarta el tracking del primer
        # write; ejecutar el precommit aquí lo limpia (detalle de Odoo 19).
        self.env.cr.precommit.run()
        message = booking.message_post(body=Markup('<p>Hola</p>'))
        self.assertTrue(message.id, 'EJERCICIO 33: message_post debe crear un mensaje')
        booking.state = 'ongoing'
        # En Odoo 19 los mensajes de tracking se generan en un hook de
        # precommit; en tests hay que forzarlo antes de comprobarlos.
        self.env.cr.precommit.run()
        tracked = booking.message_ids.filtered(lambda m: m.tracking_value_ids)
        self.assertTrue(
            tracked,
            'EJERCICIO 33: añade tracking=True al campo state',
        )

    def test_ex34_wizard(self):
        wizard = self.Wizard.create({
            'membership_id': self.membership.id,
            'partner_id': self.partner.id,
            'date_start': fields.Date.today(),
            'date_end': fields.Date.today() + timedelta(days=3),
        })
        action = wizard.action_create_booking()
        self.assertIsInstance(action, dict, 'EJERCICIO 34: debe devolver un dict de acción')
        self.assertEqual(
            action.get('res_model'), 'cd.gym.booking',
            'EJERCICIO 34: la acción debe abrir cd.gym.booking',
        )
        booking = self.Booking.browse(action.get('res_id'))
        self.assertTrue(booking.exists(), 'EJERCICIO 34: la reserva debe existir')
        self.assertEqual(booking.membership_id, self.membership, 'EJERCICIO 34: cuota de la reserva')
        self.assertEqual(booking.partner_id, self.partner, 'EJERCICIO 34: socio de la reserva')
        self.assertEqual(
            booking.date_end, fields.Date.today() + timedelta(days=3),
            'EJERCICIO 34: fecha de fin de la reserva',
        )

    def test_ex35_cron(self):
        cron = self.env.ref(
            'cd_gym_practices.ir_cron_cd_gym_cancel_expired_bookings',
            raise_if_not_found=False,
        )
        self.assertTrue(
            cron,
            'EJERCICIO 35: no existe el cron ir_cron_cd_gym_cancel_expired_bookings',
        )
        expired = self.Booking.create({
            'name': 'Caducada',
            'membership_id': self.membership.id,
            'partner_id': self.partner.id,
            'state': 'ongoing',
            'date_end': fields.Date.today() - timedelta(days=1),
        })
        current = self.Booking.create({
            'name': 'Vigente',
            'membership_id': self.membership.id,
            'partner_id': self.partner.id,
            'state': 'ongoing',
            'date_end': fields.Date.today() + timedelta(days=1),
        })
        self.Booking._cron_cancel_expired_bookings()
        self.assertEqual(
            expired.state, 'cancelled',
            'EJERCICIO 35: la reserva caducada debe cancelarse',
        )
        self.assertEqual(
            current.state, 'ongoing',
            'EJERCICIO 35: la reserva vigente no debe tocarse',
        )
