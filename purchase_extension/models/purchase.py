from odoo import models, fields, api

class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    category_id= fields.Many2one('product.category','Product Category',related="product_tmpl_id.categ_id",store=True)

