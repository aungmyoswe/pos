from odoo import api, fields, models, _

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"
    
    @api.depends('price_unit', 'tax_ids', 'qty', 'discount', 'product_id')
    def _compute_amount_line_all(self):
        for line in self:
            fpos = line.order_id.fiscal_position_id
            tax_ids_after_fiscal_position = fpos.map_tax(line.tax_ids, line.product_id, line.order_id.partner_id) if fpos else line.tax_ids
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = tax_ids_after_fiscal_position.compute_all(price, line.order_id.pricelist_id.currency_id, line.qty, product=line.product_id, partner=line.order_id.partner_id)
            margin = line.price_unit - line.product_id.product_tmpl_id.standard_price    
            line.update({
                'price_subtotal_incl': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
                'margin': margin,
            })
                         
    margin = fields.Float(compute='_compute_amount_line_all', string='Margin', store=True)
    purchase_price = fields.Float(related='product_id.product_tmpl_id.standard_price', store=True,string='Cost')
    
class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.depends('statement_ids', 'lines.price_subtotal_incl', 'lines.discount')
    def _compute_amount_all(self):
        for order in self:
            order.amount_paid = order.amount_return = order.amount_tax = 0.0
            currency = order.pricelist_id.currency_id
            order.amount_paid = sum(payment.amount for payment in order.statement_ids)
            order.amount_return = sum(payment.amount < 0 and payment.amount or 0 for payment in order.statement_ids)
            order.amount_tax = currency.round(sum(self._amount_line_tax(line, order.fiscal_position_id) for line in order.lines))
            amount_untaxed = currency.round(sum(line.price_subtotal for line in order.lines))
            order.amount_total = order.amount_tax + amount_untaxed
            order.margin = sum(line.margin for line in order.lines)
            
    margin = fields.Float(compute='_compute_amount_all', string='Margin', store=True)