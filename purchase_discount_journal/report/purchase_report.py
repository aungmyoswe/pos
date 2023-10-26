from odoo import api, fields, models, tools

class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    total_discount = fields.Float('Discount Total', readonly=True, group_operator="sum")
    dis_amount = fields.Float("Discont Average", readonly=True, group_operator="avg")
    average_price_unit = fields.Float("AD Unit Price", readonly=True, group_operator="avg")

    def _select(self):
    	select_str = super()._select()
    	select_str += """
    		,l.line_dis_total_amount as total_discount
    		,l.line_dis_total_amount/l.product_qty as dis_amount
    		,sum(((l.price_unit / COALESCE(NULLIF(cr.rate, 0), 1.0) * l.product_qty)-l.line_dis_total_amount)/(l.product_qty/u.factor*u2.factor))::decimal(16,2) as average_price_unit """
    	return select_str

    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += """
        	,l.dis_amount
        	,l.product_qty
        	,l.line_dis_total_amount
        	"""
        return group_by_str