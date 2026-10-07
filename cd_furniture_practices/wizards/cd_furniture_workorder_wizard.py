from odoo import fields, models


class CdFurnitureWorkorderWizard(models.TransientModel):
    """Asistente (TransientModel) para crear una orden desde un mueble."""

    _name = 'cd.furniture.workorder.wizard'
    _description = 'Asistente de fabricación'

    product_id = fields.Many2one('cd.furniture.product', string='Mueble', required=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    date_start = fields.Date(string='Fecha de inicio', required=True)
    date_end = fields.Date(string='Fecha de fin', required=True)

    # =========================================================================
    # EJERCICIO 34 · Bloque 6 · Test: TestMailWizardCron.test_ex34_wizard
    # -------------------------------------------------------------------------
    # Implementa action_create_workorder():
    #   1) Crea una orden con los datos del asistente (product_id, partner_id,
    #      date_start, date_end).
    #   2) Devuelve un dict ir.actions.act_window que abra esa orden en
    #      vista form sobre la ventana actual (target 'current').
    # PISTA DE SINTAXIS
    #   workorder = self.env['cd.furniture.workorder'].create({
    #       'product_id': self.product_id.id,
    #       ...
    #   })
    #   return {
    #       'type': 'ir.actions.act_window',
    #       'res_model': 'cd.furniture.workorder',
    #       'res_id': workorder.id,
    #       'view_mode': 'form',
    #       'target': 'current',
    #   }
    # =========================================================================
    def action_create_workorder(self):
        raise NotImplementedError('EJERCICIO 34 pendiente: create + act_window')
