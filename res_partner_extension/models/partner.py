# See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, tools, _
from odoo.tools import pycompat

class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_name = fields.Char("Contact Name")
   