from odoo import fields, models


class CdPracticeBookingWizard(models.TransientModel):
    """Asistente (TransientModel) para crear una reserva desde un elemento."""

    _name = 'cd.practice.booking.wizard'
    _description = 'Asistente de reserva'

    item_id = fields.Many2one('cd.practice.item', string='Elemento', required=True)
    partner_id = fields.Many2one('res.partner', string='Solicitante', required=True)
    date_start = fields.Date(string='Fecha de inicio', required=True)
    date_end = fields.Date(string='Fecha de fin', required=True)

    # =========================================================================
    # EJERCICIO 34 · Bloque 6 · Test: TestMailWizardCron.test_ex34_wizard
    # -------------------------------------------------------------------------
    # Implementa action_create_booking():
    #   1) Crea una reserva con los datos del asistente (item_id, partner_id,
    #      date_start, date_end).
    #   2) Devuelve un dict ir.actions.act_window que abra esa reserva en
    #      vista form sobre la ventana actual (target 'current').
    # PISTA DE SINTAXIS
    #   booking = self.env['cd.practice.booking'].create({
    #       'item_id': self.item_id.id,
    #       ...
    #   })
    #   return {
    #       'type': 'ir.actions.act_window',
    #       'res_model': 'cd.practice.booking',
    #       'res_id': booking.id,
    #       'view_mode': 'form',
    #       'target': 'current',
    #   }
    # =========================================================================
    def action_create_booking(self):
        raise NotImplementedError('EJERCICIO 34 pendiente: create + act_window')
