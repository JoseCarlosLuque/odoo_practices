from odoo import fields, models


class CdVetVisitWizard(models.TransientModel):
    """Asistente (TransientModel) para crear una visita desde una mascota."""

    _name = 'cd.vet.visit.wizard'
    _description = 'Asistente de visita'

    pet_id = fields.Many2one('cd.vet.pet', string='Mascota', required=True)
    partner_id = fields.Many2one('res.partner', string='Dueño', required=True)
    date_start = fields.Date(string='Fecha de inicio', required=True)
    date_end = fields.Date(string='Fecha de fin', required=True)

    # =========================================================================
    # EJERCICIO 34 · Bloque 6 · Test: TestMailWizardCron.test_ex34_wizard
    # -------------------------------------------------------------------------
    # Implementa action_create_visit():
    #   1) Crea una visita con los datos del asistente (pet_id, partner_id,
    #      date_start, date_end).
    #   2) Devuelve un dict ir.actions.act_window que abra esa visita en
    #      vista form sobre la ventana actual (target 'current').
    # PISTA DE SINTAXIS
    #   visit = self.env['cd.vet.visit'].create({
    #       'pet_id': self.pet_id.id,
    #       ...
    #   })
    #   return {
    #       'type': 'ir.actions.act_window',
    #       'res_model': 'cd.vet.visit',
    #       'res_id': visit.id,
    #       'view_mode': 'form',
    #       'target': 'current',
    #   }
    # =========================================================================
    def action_create_visit(self):
        raise NotImplementedError('EJERCICIO 34 pendiente: create + act_window')
