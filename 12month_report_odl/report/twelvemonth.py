# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from io import StringIO
import io
import json
import time
import xlsxwriter
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class TwelveMonthReport(models.AbstractModel):
    _name = 'report.12month_report.twelve_month_xlsx_report'

    @api.model
    def get_report_values(self, docids, data=None):
        self.product_qty = 0.0
        self.total_inventory = []
        return {
        		'doc_ids': self._ids,
        		'docs': self,
        		'data': data,
        		'time': time,
        		}

    def convert_withtimezone(self, userdate):
        """ 
        Convert to Time-Zone with compare to UTC
        """
        user_date = datetime.strptime(userdate, DEFAULT_SERVER_DATETIME_FORMAT)
        tz_name = self.env.context.get('tz') or self.env.user.tz
        if tz_name:
            utc = pytz.timezone('UTC')
            context_tz = pytz.timezone(tz_name)
            # not need if you give default datetime into entry ;)
            user_datetime = user_date  # + relativedelta(hours=24.0)
            local_timestamp = context_tz.localize(user_datetime, is_dst=False)
            user_datetime = local_timestamp.astimezone(utc)
            return user_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return user_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def _get_quantity_value(self, date, locations , filter_product_ids=[]):
    	self._cr.execute('''SELECT pp.id,pp.default_code,par.name as supplier,pt.name as product, pb.name as Brand,t.code,
						CASE WHEN pt.uom_id = m.product_uom 
						THEN pu.name 
						ELSE (select name from uom_uom where id = pt.uom_id) end AS name,
						CASE WHEN pt.uom_id = m.product_uom 
						THEN coalesce(sum(m.product_qty)::decimal, 0.0)
						ELSE coalesce(sum(m.product_qty)::decimal, 0.0) END  AS qty
						FROM product_product pp
						LEFT JOIN stock_move m ON (m.product_id=pp.id)
						LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
						LEFT JOIN stock_location l on(m.location_dest_id=l.id)    
						LEFT JOIN stock_picking p ON (m.picking_id=p.id)
						LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id)
						LEFT JOIN uom_uom pu ON (pt.uom_id=pu.id)
						LEFT JOIN product_brand pb ON(pb.id = pt.product_brand_id)
						LEFT JOIN res_partner par ON (par.id = pt.supplier_id)
						WHERE m.state='done' and pp.active=True
						AND date_part('year', m.date) = '2019'
						AND date_part('month', m.date) = '06'
						AND t.code = 'outgoing'
						GROUP BY  pp.id,pt.uom_id , m.product_uom ,
						pp.default_code,pu.name,par.name,pt.name,pb.name,t.code
						 ''',())
    	values = self._cr.dictfetchall()
    	return values

    def get_report_name(self):
    	return _('Twelve Month Report By Warehouse')

    def find_warehouses(self,company_id):
        """
        Find all warehouses
        """
        return [x.id for x in self.env['stock.warehouse'].search([('company_id','=',company_id)])]


    def get_report_filename(self, options):
        """The name that will be used for the file when downloading pdf,xlsx,..."""
        return self.get_report_name().lower().replace(' ', '_')

    def get_header_name(self):
        return _('Inventory Report')

    def _product_name(self, product_id):
        """
        Find product name and assign to it
        """
        product = self.env['product.product'].browse(product_id).name_get()
        return product and product[0] and product[0][1] or ''

    def _product_code(self, product_id):
        """
        Find product name and assign to it
        """
        product = self.env['product.product'].browse(product_id)
        return product.default_code or ''

    def _product_brand(self, product_id):
        """
        Find product name and assign to it
        """
        product = self.env['product.product'].browse(product_id)
        return product.product_brand_id.name or ''

    # def _supplier_name(self, product_id):
    #     """
    #     Find product name and assign to it
    #     """
    #     product = self.env['product.product'].browse(product_id)
    #     return product.supplier_id.name or ''

    # def _product_category_name(self, product_id):
   	# 	"""
    #     Find product name and assign to it
    #     """
    #     product = self.env['product.product'].browse(product_id)
    #     return product.categ_id.name or ''

    # def _product_sale_price(self, product_id):
    #     """
    #     Find product name and assign to it
    #     """
    #     product = self.env['product.product'].browse(product_id)
    #     return product.list_price or ''

    # def _product_cost_price(self, product_id):
    #     """
    #     Find product name and assign to it
    #     """
    #     product = self.env['product.product'].browse(product_id)
    #     return product.standard_price or ''

    def _find_locations(self, warehouse):
        """
        Find warehouse stock locations and its childs.
            -All stock reports depends on stock location of warehouse.
        """
        warehouse_obj = self.env['stock.warehouse']
        location_obj = self.env['stock.location']
        store_location_id = warehouse_obj.browse(warehouse).view_location_id.id
        return [x.id for x in location_obj.search([('location_id', 'child_of', store_location_id)])]

    def _compare_with_company(self, warehouse, company):
        """
        Company loop check ,whether it is in company of not.
        """
        company_id = self.env['stock.warehouse'].browse(warehouse).read(['company_id'])[0]['company_id']
        if company_id[0] != company:
            return False
        return True

    def _get_lines(self, data, company):
        """
        Process:
            Pass start date, end date, locations to get data from moves,
            Merge those data with locations,
        Return:
            {location : [{},{},{}...], location : [{},{},{}...],...}
        """
        date = self.convert_withtimezone(data['form']['date']+' 00:00:00')
        warehouse_ids = data['form'] and data['form'].get('warehouse_ids',[]) or []
        filter_product_ids = data['form'] and data['form'].get('filter_product_ids') or []
        location_id = data['form'] and data['form'].get('location_id') or False
        if not warehouse_ids:
            warehouse_ids = self.find_warehouses(company)

        final_values = {}
        for warehouse in warehouse_ids:
            #looping for only warehouses which is under current company
            if self._compare_with_company(warehouse, company[0]):
                locations = self._find_locations(warehouse)
                if location_id:
                    if (location_id in locations):
                        final_values.update({
                                             warehouse:self._get_quantity_value(date, [location_id],filter_product_ids)
                                             })
                else:
                    final_values.update({
                                         warehouse:self._get_quantity_value(date, locations,filter_product_ids)
                                         })
        self.value_exist = final_values
        return final_values

    def xlsx_export(self,datas):  
        return {
                    'type': 'ir_actions_account_report_download',
                    'data': {'model': 'report.12month_report.twelve_month_xlsx_report',
                    'options': json.dumps(datas, indent=4, sort_keys=True, default=str),
                    'output_format': 'xlsx',
                    'financial_id': self.env.context.get('id'),
                    }
                }

    @api.multi
    def get_xlsx(self, options,response):
    	output = io.BytesIO()
    	get_lines=[]
    	workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    	sheet = workbook.add_worksheet(self.get_report_name()[:31])
    	self._define_formats(workbook)
    	sheet.set_column(0, 0, 15) #  Set the first column width to 15
    	get_lines=self.get_report_values(self._ids, options)
    	company_name = warehouse_name =warehouse_name_group =''
    	cid=options['form']['company_id']
    	if cid:
    		for company in self.env['res.company'].browse(cid).name_get():
    			company_name += str(company[1]) + ','
    		company_name = company_name[:-1]
    	else:
    		company_name = 'All'
    	warehouse_id = options['form']['warehouse_ids']
    	if warehouse_id:
    		for warehouse in self.env['stock.warehouse'].browse(warehouse_id).name_get():
    			warehouse_name += (warehouse[1] + ',')
    		warehouse_name = warehouse_name[:-1]
    	else:
    		warehouse_name = 'All'
    	y_offset = 0
    	x = 0
    	sheet.merge_range(y_offset, 9, y_offset, 12, _('Twelve Month Report'), self.format_title)
    	y_offset += 2
    	sheet.write(y_offset, 0, _('Item Code') or '', self.format_header_center)
    	sheet.write(y_offset, 1, _('Product Name') or '', self.format_header_center)
    	sheet.write(y_offset, 2, _('UOM') or '', self.format_header_center)
    	sheet.write(y_offset, 3, _('Brand Name') or '', self.format_header_center)
    	sheet.write(y_offset, 4, _('Parent Category') or '', self.format_header_center)
    	sheet.write(y_offset, 5, _('Child Category') or '', self.format_header_center)
    	sheet.write(y_offset, 6, _('Supplier Name') or '', self.format_header_center)
    	sheet.write(y_offset, 7, _('Sales Price') or '', self.format_header_right)
    	sheet.write(y_offset, 8, _('Cost Price') or '', self.format_header_center)
    	sheet.write(y_offset, 9, _('Month 12') or '', self.format_header_center)
    	sheet.write(y_offset, 10, _('Month 11') or '', self.format_header_center)
    	sheet.write(y_offset, 11, _('Month 10') or '', self.format_header_center)
    	sheet.write(y_offset, 12, _('Month 9') or '', self.format_header_center)
    	sheet.write(y_offset, 13, _('Month 8') or '', self.format_header_center)
    	sheet.write(y_offset, 14, _('Month 7') or '', self.format_header_center)
    	sheet.write(y_offset, 15, _('Month 6') or '', self.format_header_center)
    	sheet.write(y_offset, 16, _('Month 5') or '', self.format_header_center)
    	sheet.write(y_offset, 17, _('Month 4') or '', self.format_header_center)
    	sheet.write(y_offset, 18, _('Month 3') or '', self.format_header_center)
        sheet.write(y_offset, 19, _('Month 2') or '', self.format_header_center) 
        sheet.write(y_offset, 20, _('Month 1') or '', self.format_header_center)
        
    @api.multi
    def _define_formats(self, workbook):
        self.format_title_company = workbook.add_format({
            'bold': True,
            'align': 'center',
        })
        self.format_title_data = workbook.add_format({
            'border': True,
            'align': 'center',
        })
        self.format_title = workbook.add_format({
            'bold': True,
            'align': 'center',
            'font_size': 14,
        })
        self.format_header = workbook.add_format({
            'bold': True,
            'bg_color': '#FFFFCC',
            'border': True
        })
        self.format_header_right = workbook.add_format({
            'bold': True,
            'bg_color': '#FFFFCC',
            'border': True,
            'align': 'right'
        })
        self.format_header_center = workbook.add_format({
            'bold': True,
            'bg_color': '#FFFFCC',
            'border': True,
            'align': 'center'
        })
        self.format_header_italic = workbook.add_format({
            'bold': True,
            'bg_color': '#FFFFCC',
            'border': True,
            'italic': True
        })
        self.format_border_top = workbook.add_format({
            'border': True,
            'align': 'center'
        })
        self.product_format = workbook.add_format({
            'border': True,
            'align': 'left'
        })
        self.format_header_one = workbook.add_format({
            'align': 'center',
            'bold': True,
            'border': True,
        })