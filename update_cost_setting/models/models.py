# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_company(models.Model):
    _inherit = "res.company"

    account_chart_id = fields.Many2one("account.account", string="Counter-Part Account")
    

class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'
    _inherit = 'res.config.settings'

    account_chart_id = fields.Many2one('account.account', related="company_id.account_chart_id", readonly=False,string="Counter-Part Account", help="Sale Discount of the company.")

    @api.onchange('company_id')
    def onchange_company_id(self):
        self.account_chart_id = self.company_id.account_chart_id
       