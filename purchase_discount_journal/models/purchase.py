from odoo import api, fields, models, SUPERUSER_ID,_
from odoo.exceptions import UserError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.one
    @api.depends('discount_type','discount_rate','order_line.price_total','is_tax')
    def _amount_all(self):
        for order in self:
            amt_total = amount_discount  = amount_untaxed = amount_tax = amount_dis_total = self.amount_discount = self.amount_tax = line_discount= 0.0
            for line in order.order_line:
                if line.discount_line_type == 'fixed':
                    line_discount += (line.dis_amount * line.product_qty)
                    line.line_dis_total_amount = (line.dis_amount * line.product_qty)
                elif line.discount_line_type == 'percent':
                    line_discount += ((line.product_qty * line.price_unit) * line.dis_amount)/100
                    line.line_dis_total_amount = (line.product_qty * line.price_unit * line.dis_amount)/100
                else:
                    line_discount = line_discount

                if self.discount_type == 'fixed':
                    amount_untaxed  += line.price_subtotal 
                    self.amount_untaxed = amount_untaxed 
                    line.discount = 0.0
                    amount_discount = self.discount_rate
                elif self.discount_type == 'percent':
                    amount_untaxed += line.product_qty * line.price_unit
                    self.amount_untaxed = amount_untaxed
                    amount_discount += ((line.product_qty * line.price_unit) * self.discount_rate)/100
                else:
                    amount_untaxed  += line.price_subtotal 
                    self.amount_untaxed = amount_untaxed
                    self.amount_discount = 0.0
                    self.discount_rate = 0.0
        amount_discount = amount_discount + line_discount
        amount_dis_total = amount_untaxed - amount_discount
        if self.company_id.global_tax == True and self.is_tax == True:
            if self.company_id.account_purchase_tax_id:
                amount_tax = (amount_dis_total*self.company_id.account_purchase_tax_id.amount)/100
            else:
                raise UserError(_('Please check purchase account tax.'))
        else:
            amount_tax = 0.0
        amt_total = amount_dis_total + amount_tax
        order.update({
            'amount_untaxed': order.currency_id.round(amount_untaxed),
            'amount_tax': order.currency_id.round(amount_tax),
            'amount_discount':order.currency_id.round(amount_discount),
            'amount_dis_total':order.currency_id.round(amount_dis_total),
            'amount_total':amt_total,
        })

    is_tax = fields.Boolean("Is Tax", default=True, store=True)
    global_tax = fields.Boolean("Global Tax", related="company_id.global_tax",store=True)
    discount_type = fields.Selection([('fixed',"Fixed"),('percent',"Percentage")],default="fixed",string="Type")
    discount_rate = fields.Float("Discount")
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_all')
    amount_dis_total = fields.Monetary(string='After Discount Total', store=True, readonly=True, compute='_amount_all')

    @api.onchange('discount_type')
    def onchange_discount_type(self):
        self.discount_rate = 0.0
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount_line_type = fields.Selection([('fixed',"Fixed"),('percent',"Percentage")], string="Discount Type", default='percent')
    dis_amount = fields.Float(string='Discount', digits=(16, 2), store=True)
    line_dis_total_amount = fields.Float(string="Total Discount", digits=(16, 2), store=True)