from odoo import api, fields, models


class CdFurnitureWorkorder(models.Model):
    """Orden de fabricación. Se usa en los bloques 5 (seguridad) y 6 (mail/cron)."""

    _name = 'cd.furniture.workorder'
    _description = 'Orden de fabricación'

    name = fields.Char(string='Referencia', required=True, default='Orden')
    product_id = fields.Many2one(
        'cd.furniture.product',
        string='Mueble',
        required=True,
        ondelete='cascade',
    )
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    date_start = fields.Date(string='Fecha de inicio')
    date_end = fields.Date(string='Fecha de fin')
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('ongoing', 'En curso'),
            ('done', 'Finalizada'),
            ('cancelled', 'Cancelada'),
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
    #   3) En views/cd_furniture_workorder_views.xml descomenta <chatter/>.
    # El test comprueba que existe message_post y que al cambiar el estado se
    # genera un mensaje con tracking_value_ids.
    # =========================================================================

    # =========================================================================
    # EJERCICIO 35 · Bloque 6 · Test: TestMailWizardCron.test_ex35_cron
    # -------------------------------------------------------------------------
    # a) Implementa _cron_cancel_expired_workorders(): busca las órdenes en
    #    estado 'ongoing' cuya date_end sea ANTERIOR a hoy y pásalas a
    #    'cancelled' con una sola escritura.
    #    PISTA: self.search([('state', '=', 'ongoing'),
    #                        ('date_end', '<', fields.Date.today())])
    # b) Crea el XML del cron en data/cd_furniture_cron.xml (hay instrucciones
    #    dentro de ese archivo).
    # =========================================================================
    @api.model
    def _cron_cancel_expired_workorders(self):
        raise NotImplementedError('EJERCICIO 35 pendiente: search + write y el XML del cron')
