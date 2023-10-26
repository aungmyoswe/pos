from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = "product.product"

    supplier_id = fields.Many2one('res.partner', 'Supplier', domain=[('supplier', '=', True)])
    


class ProductTemplate(models.Model):
   _inherit = "product.template"

   supplier_id = fields.Many2one('res.partner','Supplier', domain=[('supplier', '=', True)])