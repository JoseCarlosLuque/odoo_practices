from datetime import timedelta

from markupsafe import Markup

from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('cd_vet_practice', '-standard')
class TestMailWizardCron(TransactionCase):
    """Bloque 6 · Mail, wizards y crons (ejercicios 33 a 35)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Visit = cls.env['cd.vet.visit']
        cls.Pet = cls.env['cd.vet.pet']
        cls.Wizard = cls.env['cd.vet.visit.wizard']
        cls.partner = cls.env['res.partner'].create({'name': 'Dueño'})
        cls.pet = cls.Pet.create({'name': 'Mascota visitable'})

    def test_ex33_mail_thread(self):
        self.assertTrue(
            hasattr(self.Visit, 'message_post'),
            'EJERCICIO 33: cd.vet.visit debe heredar de mail.thread',
        )
        visit = self.Visit.create({
            'name': 'Visita mail',
            'pet_id': self.pet.id,
            'partner_id': self.partner.id,
        })
        # create() deja un marcador interno que descarta el tracking del primer
        # write; ejecutar el precommit aquí lo limpia (detalle de Odoo 19).
        self.env.cr.precommit.run()
        message = visit.message_post(body=Markup('<p>Hola</p>'))
        self.assertTrue(message.id, 'EJERCICIO 33: message_post debe crear un mensaje')
        visit.state = 'scheduled'
        # En Odoo 19 los mensajes de tracking se generan en un hook de
        # precommit; en tests hay que forzarlo antes de comprobarlos.
        self.env.cr.precommit.run()
        tracked = visit.message_ids.filtered(lambda m: m.tracking_value_ids)
        self.assertTrue(
            tracked,
            'EJERCICIO 33: añade tracking=True al campo state',
        )

    def test_ex34_wizard(self):
        wizard = self.Wizard.create({
            'pet_id': self.pet.id,
            'partner_id': self.partner.id,
            'date_start': fields.Date.today(),
            'date_end': fields.Date.today() + timedelta(days=3),
        })
        action = wizard.action_create_visit()
        self.assertIsInstance(action, dict, 'EJERCICIO 34: debe devolver un dict de acción')
        self.assertEqual(
            action.get('res_model'), 'cd.vet.visit',
            'EJERCICIO 34: la acción debe abrir cd.vet.visit',
        )
        visit = self.Visit.browse(action.get('res_id'))
        self.assertTrue(visit.exists(), 'EJERCICIO 34: la visita debe existir')
        self.assertEqual(visit.pet_id, self.pet, 'EJERCICIO 34: mascota de la visita')
        self.assertEqual(visit.partner_id, self.partner, 'EJERCICIO 34: dueño de la visita')
        self.assertEqual(
            visit.date_end, fields.Date.today() + timedelta(days=3),
            'EJERCICIO 34: fecha de fin de la visita',
        )

    def test_ex35_cron(self):
        cron = self.env.ref(
            'cd_vet_practices.ir_cron_cd_vet_cancel_expired_visits',
            raise_if_not_found=False,
        )
        self.assertTrue(
            cron,
            'EJERCICIO 35: no existe el cron ir_cron_cd_vet_cancel_expired_visits',
        )
        expired = self.Visit.create({
            'name': 'Caducada',
            'pet_id': self.pet.id,
            'partner_id': self.partner.id,
            'state': 'scheduled',
            'date_end': fields.Date.today() - timedelta(days=1),
        })
        current = self.Visit.create({
            'name': 'Vigente',
            'pet_id': self.pet.id,
            'partner_id': self.partner.id,
            'state': 'scheduled',
            'date_end': fields.Date.today() + timedelta(days=1),
        })
        self.Visit._cron_cancel_expired_visits()
        self.assertEqual(
            expired.state, 'cancelled',
            'EJERCICIO 35: la visita caducada debe cancelarse',
        )
        self.assertEqual(
            current.state, 'scheduled',
            'EJERCICIO 35: la visita vigente no debe tocarse',
        )
