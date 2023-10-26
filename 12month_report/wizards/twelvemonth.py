# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)

import time
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from dateutil import parser
import xlsxwriter
from odoo.exceptions import Warning
from odoo import models, fields, api, _

class TwelveMonthReport(models.TransientModel):
    _name = "twelve.month.report"
    
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.user.company_id)
    warehouse_ids = fields.Many2many('stock.warehouse', string='warehouse')
    location_id = fields.Many2one('stock.location', string='Location')
    date = fields.Date('Beginning Date', required=True, default= lambda *a:datetime.now().strftime('%Y-%m-%d'))
    filter_product_ids = fields.Many2many('product.product', string='Products')

    @api.multi
    def print_report_xlsx(self):
        data_obj = self.env['report.12month_report.twelve_month_xlsx_report']
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        datas = {'form':{
            'company_id': self.company_id and [self.company_id.id] or [],
            'warehouse_ids': [y.id for y in self.warehouse_ids],
            'location_id': self.location_id and self.location_id.id or False,
            'date': self.date,
            'id': self.id,
            'filter_product_ids': [p.id for p in self.filter_product_ids]}}
        if [y.id for y in self.warehouse_ids] and (not self.company_id):
            self.warehouse_ids = []
            raise Warning(_('Please select company of those warehouses to get correct view.\nYou should remove all warehouses first from selection field.'))
        return data_obj.xlsx_export(datas)