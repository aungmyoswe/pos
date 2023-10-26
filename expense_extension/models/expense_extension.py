from odoo import models, fields, api

class HrExpense(models.Model):
   _inherit = 'hr.expense'

   quantity = fields.Float(required=True, readonly=True, default=1)

class HrExpenseSheet(models.Model):
	_inherit="hr.expense.sheet"

	voucher_no = fields.Char(string="Voucher No",store=True,require=True)