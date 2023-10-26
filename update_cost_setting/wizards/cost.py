from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class StockChangeStandardPrice(models.TransientModel):
    _inherit = "stock.change.standard.price"

    def _account_get(self):
        if self.env.user.company_id.account_chart_id:
            return self.env.user.company_id.account_chart_id

    counterpart_account_id = fields.Many2one('account.account',default=_account_get, readonly=True, string="Counter-Part Account", domain=[('deprecated', '=', False)])