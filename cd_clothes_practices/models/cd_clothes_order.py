from odoo import api, fields, models


class CdClothesOrder(models.Model):
    """Pedido de una prenda. Se usa en los bloques 5 (seguridad) y 6 (mail/cron)."""

    _name = 'cd.clothes.order'
    _description = 'Pedido de tienda'

    name = fields.Char(string='Referencia', required=True, default='Pedido')
    product_id = fields.Many2one(
        'cd.clothes.product',
        string='Prenda',
        required=True,
        ondelete='cascade',
    )
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    date_start = fields.Date(string='Fecha del pedido')
    date_end = fields.Date(string='Fecha de entrega')
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('ongoing', 'En curso'),
            ('shipped', 'Enviado'),
            ('cancelled', 'Cancelado'),
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
    #   3) En views/cd_clothes_order_views.xml descomenta <chatter/>.
    # El test comprueba que existe message_post y que al cambiar el estado se
    # genera un mensaje con tracking_value_ids.
    # =========================================================================

    # =========================================================================
    # EJERCICIO 35 · Bloque 6 · Test: TestMailWizardCron.test_ex35_cron
    # -------------------------------------------------------------------------
    # a) Implementa _cron_cancel_expired_orders(): busca los pedidos en
    #    estado 'ongoing' cuya date_end sea ANTERIOR a hoy y pásalos a
    #    'cancelled' con una sola escritura.
    #    PISTA: self.search([('state', '=', 'ongoing'),
    #                        ('date_end', '<', fields.Date.today())])
    # b) Crea el XML del cron en data/cd_clothes_cron.xml (hay instrucciones
    #    dentro de ese archivo).
    # =========================================================================
    @api.model
    def _cron_cancel_expired_orders(self):
        raise NotImplementedError('EJERCICIO 35 pendiente: search + write y el XML del cron')
