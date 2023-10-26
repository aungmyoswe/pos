# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from io import StringIO
import io
import json
import time
import xlsxwriter
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

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

    def _get_12quantity_value(self, date, locations , filter_product_ids=[]):
        vals = []
        added_date =  month = year = None
        added_date = date
        added_date = datetime.strptime(added_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=12)
        mon1 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=1)
        mon2 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=2)
        mon3 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=3)
        mon4 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=4)
        mon5 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=5)
        mon6 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=6)
        mon7= datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=7)
        mon8 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=8)
        mon9= datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=9)
        mon10 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=10)
        mon11 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=11)
        if len(str(added_date.month))==2:
            month = added_date.month
        else:
            month = '0'+str(added_date.month)
        year = str(added_date.year)
        if len(str(mon1.month))==2:
            month1 = mon1.month
        else:
            month1 = '0'+str(mon1.month)
        year1 = mon1.year
        if len(str(mon2.month))==2:
            month2 = mon2.month
        else:
            month2 = '0'+str(mon2.month)
        year2 = mon2.year
        if len(str(mon3.month))==2:
            month3 = mon3.month
        else:
            month3 = '0'+str(mon3.month)
        year3 = mon3.year
        if len(str(mon4.month))==2:
            month4 = mon4.month
        else:
            month4= '0'+str(mon4.month)
        year4= mon4.year
        if len(str(mon5.month))==2:
            month5 = mon5.month
        else:
            month5= '0'+str(mon5.month)
        year5= mon5.year
        if len(str(mon6.month))==2:
            month6 = mon6.month
        else:
            month6= '0'+str(mon6.month)
        year6= mon6.year
        if len(str(mon7.month))==2:
            month7 = mon7.month
        else:
            month7= '0'+str(mon7.month)
        year7= mon7.year
        if len(str(mon8.month))==2:
            month8 = mon8.month
        else:
            month8= '0'+str(mon8.month)
        year8= mon8.year
        if len(str(mon9.month))==2:
            month9= mon9.month
        else:
            month9= '0'+str(mon9.month)
        year9= mon9.year
        if len(str(mon10.month))==2:
            month10= mon10.month
        else:
            month10= '0'+str(mon10.month)
        year10= mon10.year
        if len(str(mon11.month))==2:
            month11= mon11.month
        else:
            month11= '0'+str(mon11.month)
        year11= mon11.year
        if not filter_product_ids:
            raise UserError(_('Product Line does not exit please select product.'))
        print("location",locations)
        self._cr.execute('''SELECT pt.name,pc.name as categ,pc.parent_id as parent,pt.list_price as list_price, pp.id,pp.default_code,par.name as supplier,pt.name as product, pb.name as brand,t.code,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty1,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty2,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty3,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty4,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty5,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty6,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty7,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty8,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty9,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty10,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty11,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) WHERE t.code='outgoing' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s AND sm.product_id = pp.id) as qty12,
            CASE WHEN pt.uom_id = m.product_uom 
            THEN pu.name 
            ELSE (select name from uom_uom where id = pt.uom_id) end AS uom
            FROM product_product pp
                LEFT JOIN stock_move m ON (m.product_id=pp.id)
                LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                LEFT JOIN stock_location l ON (m.location_id=l.id)    
                LEFT JOIN stock_picking p ON (m.picking_id=p.id)
                LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id)
                LEFT JOIN uom_uom pu ON (pt.uom_id=pu.id)
                LEFT JOIN product_brand pb ON (pb.id = pt.product_brand_id)
                LEFT JOIN res_partner par ON (par.id = pt.supplier_id)
                LEFT JOIN product_category pc ON (pc.id = pt.categ_id)
                WHERE m.state='done' and pp.active=True
                AND m.date >= %s
                AND pp.id in %s
                AND m.location_id in %s
                AND t.code = 'outgoing'
                GROUP BY pp.id,pt.name,pc.name ,pc.parent_id ,pt.list_price,
                pp.id,pp.default_code,par.name,pt.name , pb.name,t.code,
                pt.uom_id,m.product_uom,pu.name
                 ''',(month,year,month1,year1,month2,year2,month3,year3,month4,year4,month5,year5,month6,year6,month7,year7,month8,year8,month9,year9,month10,year10,month11,year11,end_date,tuple(filter_product_ids),tuple(locations)))
        values = self._cr.dictfetchall()
        vals.append(values)
        return vals

    def get_report_name(self):
        return _('Twelve Month Report By Warehouse')

    def get_report_filename(self, options):
        return self.get_report_name().lower().replace(' ', '_')
        
    def find_warehouses(self,company_id):
        """
        Find all warehouses
        """
        return [x.id for x in self.env['stock.warehouse'].search([('company_id','=',company_id)])]

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
                                    warehouse:self._get_12quantity_value(date, [location_id],filter_product_ids)
                                    })

                else:
                    final_values.update({
                                    warehouse:self._get_12quantity_value(date, locations,filter_product_ids)
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
        sheet = workbook.add_worksheet(self.get_report_name())
        fromat0 = workbook.add_format({ 'bold': True,'align': 'center','font_size': 14,})
        fromat1 = workbook.add_format({ 'align': 'center', 'bold': True, 'border': True,})
        fromat2 = workbook.add_format({ 'align': 'center','border': True,})
        fromat3 = workbook.add_format({ 'align': 'left', 'border': True,})
        fromat4 = workbook.add_format({ 'align': 'right', 'border': True,})
        sheet.set_column(0, 0, 15) #  Set the first column width to 15
        company_name = warehouse_name =warehouse_name_group =''
        location_id = options['form'] and options['form'].get('location_id') or False
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
        sheet.merge_range(y_offset, 7, y_offset, 10, _('Twelve Month Report'),fromat0)
        y_offset +=2
        sheet.write(y_offset, 0, _('Item Code'),fromat1)
        sheet.write(y_offset, 1, _('Product Name'),fromat1)
        sheet.write(y_offset, 2, _('UOM'),fromat1)
        sheet.write(y_offset, 3, _('Brand Name'),fromat1)
        sheet.write(y_offset, 4, _('Parent Category'),fromat1)
        sheet.write(y_offset, 5, _('Child Category'),fromat1)
        sheet.write(y_offset, 6, _('Supplier Name'),fromat1)
        sheet.write(y_offset, 7, _('Sales Price'),fromat1)
        sheet.write(y_offset, 8, _('Cost Price'),fromat1)
        sheet.write(y_offset, 9, _('Month 12'),fromat1)
        sheet.write(y_offset, 10, _('Month 11'),fromat1)
        sheet.write(y_offset, 11, _('Month 10'),fromat1)
        sheet.write(y_offset, 12, _('Month 9'),fromat1)
        sheet.write(y_offset, 13, _('Month 8'),fromat1)
        sheet.write(y_offset, 14, _('Month 7'),fromat1)
        sheet.write(y_offset, 15, _('Month 6'),fromat1)
        sheet.write(y_offset, 16, _('Month 5'),fromat1)
        sheet.write(y_offset, 17, _('Month 4'),fromat1)
        sheet.write(y_offset, 18, _('Month 3'),fromat1)
        sheet.write(y_offset, 19, _('Month 2'),fromat1)
        sheet.write(y_offset, 20, _('Month 1'),fromat1)
        sheet.write(y_offset, 21, _('Average'),fromat1)
        sheet.write(y_offset, 22, _('On Hand'),fromat1)
        lines=self._get_lines(options,options['form']['company_id'])
        y_offset += 1
        if lines:
            for l in lines:
                for loop in lines[l]:
                    cost_price = 0
                    for line in loop:
                        avg = 0
                        product_tmpl_id = self.env['product.template'].search([('default_code','=',line['default_code']),('name','=',line['product'])])
                        price = product_tmpl_id.standard_price
                        product_id = self.env['product.product'].search([('product_tmpl_id','=',product_tmpl_id.id)])
                        parent_categ_name = self.env['product.category'].search([('id','=',line['parent'])]).complete_name
                        sq_quantity = self.env['stock.quant'].search([('product_id','=',product_id.id),('location_id','=',location_id)])
                        sheet.write(y_offset, 0, line['default_code'],fromat2)
                        sheet.write(y_offset, 1, line['product'],fromat3)
                        sheet.write(y_offset, 2, line['uom'],fromat2)
                        sheet.write(y_offset, 3, line['brand'],fromat2)
                        sheet.write(y_offset, 4, parent_categ_name,fromat2)
                        sheet.write(y_offset, 5, line['categ'],fromat2)
                        sheet.write(y_offset, 6, line['supplier'],fromat3)
                        sheet.write(y_offset, 7, line['list_price'],fromat2)
                        sheet.write(y_offset, 8, price,fromat2)
                        sheet.write(y_offset, 9, line['qty12'],fromat2)
                        if line['qty12'] != None:
                            avg += int(line['qty12'])
                        sheet.write(y_offset, 10, line['qty11'],fromat2)
                        if line['qty11'] != None:
                            avg +=int(line['qty11'])
                        sheet.write(y_offset, 11, line['qty10'],fromat2)
                        if line['qty10'] != None:
                            avg += int(line['qty10'])
                        sheet.write(y_offset, 12, line['qty9'],fromat2)
                        if line['qty9'] != None:
                            avg += int(line['qty9'])
                        sheet.write(y_offset, 13, line['qty8'],fromat2)
                        if line['qty8'] != None:
                            avg += int(line['qty8'])
                        sheet.write(y_offset, 14, line['qty7'],fromat2)
                        if line['qty7'] != None:
                            avg += int(line['qty7'])
                        sheet.write(y_offset, 15, line['qty6'],fromat2)
                        if line['qty6'] != None:
                            avg += int(line['qty6'])
                        sheet.write(y_offset, 16, line['qty5'],fromat2)
                        if line['qty5'] != None:
                            avg += int(line['qty5'])
                        sheet.write(y_offset, 17, line['qty4'],fromat2)
                        if line['qty4'] != None:
                            avg += int(line['qty4'])
                        sheet.write(y_offset, 18, line['qty3'],fromat2)
                        if line['qty3'] != None:
                            q3 += int(line['qty3'])
                        sheet.write(y_offset, 19, line['qty2'],fromat2)
                        if line['qty2'] != None:
                            avg += int(line['qty2'])
                        sheet.write(y_offset, 20, line['qty1'],fromat2)
                        if line['qty1'] != None:
                            avg += int(line['qty1'])
                        sheet.write(y_offset, 21, avg/12,fromat2)
                        sheet.write(y_offset, 22, sq_quantity.quantity,fromat2)
                        y_offset +=1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()