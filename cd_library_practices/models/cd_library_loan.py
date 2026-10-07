from odoo import api, fields, models


class CdLibraryLoan(models.Model):
    """Préstamo de un libro. Se usa en los bloques 5 (seguridad) y 6 (mail/cron)."""

    _name = 'cd.library.loan'
    _description = 'Préstamo de biblioteca'

    name = fields.Char(string='Referencia', required=True, default='Préstamo')
    book_id = fields.Many2one(
        'cd.library.book',
        string='Libro',
        required=True,
        ondelete='cascade',
    )
    partner_id = fields.Many2one('res.partner', string='Socio', required=True)
    loan_date = fields.Date(string='Fecha de préstamo')
    due_date = fields.Date(string='Fecha de devolución')
    return_date = fields.Date(string='Fecha de devolución real')
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('ongoing', 'En curso'),
            ('returned', 'Devuelto'),
            ('overdue', 'Vencido'),
        ],
        string='Estado',
        default='draft',
        required=True,
    )
    note = fields.Text(string='Notas')

    # =========================================================================
    # EJERCICIO 33 · Bloque 6 · Test: TestMailWizardCron.test_ex33_mail_thread
    # -------------------------------------------------------------------------
    # Convierte este modelo en un hilo de mensajes:
    #   1) Añade _inherit = ['mail.thread', 'mail.activity.mixin'] a la clase.
    #   2) Añade tracking=True al campo state.
    #   3) En views/cd_library_loan_views.xml descomenta <chatter/>.
    # El test comprueba que existe message_post y que al cambiar el estado se
    # genera un mensaje con tracking_value_ids.
    # =========================================================================

    # =========================================================================
    # EJERCICIO 35 · Bloque 6 · Test: TestMailWizardCron.test_ex35_cron
    # -------------------------------------------------------------------------
    # a) Implementa _cron_mark_overdue_loans(): busca los préstamos en
    #    estado 'ongoing' cuya due_date sea ANTERIOR a hoy y pásalos a
    #    'overdue' con una sola escritura.
    #    PISTA: self.search([('state', '=', 'ongoing'),
    #                        ('due_date', '<', fields.Date.today())])
    # b) Crea el XML del cron en data/cd_library_cron.xml (hay instrucciones
    #    dentro de ese archivo).
    # =========================================================================
    @api.model
    def _cron_mark_overdue_loans(self):
        raise NotImplementedError('EJERCICIO 35 pendiente: search + write y el XML del cron')
