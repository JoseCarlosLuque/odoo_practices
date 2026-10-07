from datetime import timedelta

from markupsafe import Markup

from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('cd_library_practice', '-standard')
class TestMailWizardCron(TransactionCase):
    """Bloque 6 · Mail, wizards y crons (ejercicios 33 a 35)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Loan = cls.env['cd.library.loan']
        cls.Book = cls.env['cd.library.book']
        cls.Wizard = cls.env['cd.library.loan.wizard']
        cls.partner = cls.env['res.partner'].create({'name': 'Socio'})
        cls.book = cls.Book.create({'name': 'Libro prestable'})

    def test_ex33_mail_thread(self):
        self.assertTrue(
            hasattr(self.Loan, 'message_post'),
            'EJERCICIO 33: cd.library.loan debe heredar de mail.thread',
        )
        loan = self.Loan.create({
            'name': 'Préstamo mail',
            'book_id': self.book.id,
            'partner_id': self.partner.id,
        })
        # create() deja un marcador interno que descarta el tracking del primer
        # write; ejecutar el precommit aquí lo limpia (detalle de Odoo 19).
        self.env.cr.precommit.run()
        message = loan.message_post(body=Markup('<p>Hola</p>'))
        self.assertTrue(message.id, 'EJERCICIO 33: message_post debe crear un mensaje')
        loan.state = 'ongoing'
        # En Odoo 19 los mensajes de tracking se generan en un hook de
        # precommit; en tests hay que forzarlo antes de comprobarlos.
        self.env.cr.precommit.run()
        tracked = loan.message_ids.filtered(lambda m: m.tracking_value_ids)
        self.assertTrue(
            tracked,
            'EJERCICIO 33: añade tracking=True al campo state',
        )

    def test_ex34_wizard(self):
        wizard = self.Wizard.create({
            'book_id': self.book.id,
            'partner_id': self.partner.id,
            'loan_date': fields.Date.today(),
            'due_date': fields.Date.today() + timedelta(days=3),
        })
        action = wizard.action_create_loan()
        self.assertIsInstance(action, dict, 'EJERCICIO 34: debe devolver un dict de acción')
        self.assertEqual(
            action.get('res_model'), 'cd.library.loan',
            'EJERCICIO 34: la acción debe abrir cd.library.loan',
        )
        loan = self.Loan.browse(action.get('res_id'))
        self.assertTrue(loan.exists(), 'EJERCICIO 34: el préstamo debe existir')
        self.assertEqual(loan.book_id, self.book, 'EJERCICIO 34: libro del préstamo')
        self.assertEqual(loan.partner_id, self.partner, 'EJERCICIO 34: socio del préstamo')
        self.assertEqual(
            loan.due_date, fields.Date.today() + timedelta(days=3),
            'EJERCICIO 34: fecha de devolución del préstamo',
        )

    def test_ex35_cron(self):
        cron = self.env.ref(
            'cd_library_practices.ir_cron_cd_library_mark_overdue_loans',
            raise_if_not_found=False,
        )
        self.assertTrue(
            cron,
            'EJERCICIO 35: no existe el cron ir_cron_cd_library_mark_overdue_loans',
        )
        expired = self.Loan.create({
            'name': 'Vencido',
            'book_id': self.book.id,
            'partner_id': self.partner.id,
            'state': 'ongoing',
            'due_date': fields.Date.today() - timedelta(days=1),
        })
        current = self.Loan.create({
            'name': 'Vigente',
            'book_id': self.book.id,
            'partner_id': self.partner.id,
            'state': 'ongoing',
            'due_date': fields.Date.today() + timedelta(days=1),
        })
        self.Loan._cron_mark_overdue_loans()
        self.assertEqual(
            expired.state, 'overdue',
            'EJERCICIO 35: el préstamo vencido debe marcarse como vencido',
        )
        self.assertEqual(
            current.state, 'ongoing',
            'EJERCICIO 35: el préstamo vigente no debe tocarse',
        )
