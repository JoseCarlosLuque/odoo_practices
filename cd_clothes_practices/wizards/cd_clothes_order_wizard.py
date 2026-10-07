from odoo import fields, models


class CdClothesOrderWizard(models.TransientModel):
    """Asistente (TransientModel) para crear un pedido desde una prenda."""

    _name = 'cd.clothes.order.wizard'
    _description = 'Asistente de pedido'

    product_id = fields.Many2one('cd.clothes.product', string='Prenda', required=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    date_start = fields.Date(string='Fecha del pedido', required=True)
    date_end = fields.Date(string='Fecha de entrega', required=True)

    # =========================================================================
    # EJERCICIO 34 · Bloque 6 · Test: TestMailWizardCron.test_ex34_wizard
    # -------------------------------------------------------------------------
    # Implementa action_create_order():
    #   1) Crea un pedido con los datos del asistente (product_id, partner_id,
    #      date_start, date_end).
    #   2) Devuelve un dict ir.actions.act_window que abra ese pedido en
    #      vista form sobre la ventana actual (target 'current').
    # PISTA DE SINTAXIS
    #   order = self.env['cd.clothes.order'].create({
    #       'product_id': self.product_id.id,
    #       ...
    #   })
    #   return {
    #       'type': 'ir.actions.act_window',
    #       'res_model': 'cd.clothes.order',
    #       'res_id': order.id,
    #       'view_mode': 'form',
    #       'target': 'current',
    #   }
    # =========================================================================
    def action_create_order(self):
        raise NotImplementedError('EJERCICIO 34 pendiente: create + act_window')
