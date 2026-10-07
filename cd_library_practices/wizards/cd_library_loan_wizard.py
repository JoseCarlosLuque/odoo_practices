from odoo import fields, models


class CdLibraryLoanWizard(models.TransientModel):
    """Asistente (TransientModel) para crear un préstamo desde un libro."""

    _name = 'cd.library.loan.wizard'
    _description = 'Asistente de préstamo'

    book_id = fields.Many2one('cd.library.book', string='Libro', required=True)
    partner_id = fields.Many2one('res.partner', string='Socio', required=True)
    loan_date = fields.Date(string='Fecha de préstamo', required=True)
    due_date = fields.Date(string='Fecha de devolución', required=True)

    # =========================================================================
    # EJERCICIO 34 · Bloque 6 · Test: TestMailWizardCron.test_ex34_wizard
    # -------------------------------------------------------------------------
    # Implementa action_create_loan():
    #   1) Crea un préstamo con los datos del asistente (book_id, partner_id,
    #      loan_date, due_date).
    #   2) Devuelve un dict ir.actions.act_window que abra ese préstamo en
    #      vista form sobre la ventana actual (target 'current').
    # PISTA DE SINTAXIS
    #   loan = self.env['cd.library.loan'].create({
    #       'book_id': self.book_id.id,
    #       ...
    #   })
    #   return {
    #       'type': 'ir.actions.act_window',
    #       'res_model': 'cd.library.loan',
    #       'res_id': loan.id,
    #       'view_mode': 'form',
    #       'target': 'current',
    #   }
    # =========================================================================
    def action_create_loan(self):
        raise NotImplementedError('EJERCICIO 34 pendiente: create + act_window')
