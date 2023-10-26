/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
*/
odoo.define('pos_speed_up.pos_model', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var QWeb = core.qweb;

    screens.OrderWidget.include({
        render_orderline: function (orderline) {
            var el_str = QWeb.render('Orderline', {widget: this, line: orderline});
            var el_node = $(el_str)[0];
            el_node.orderline = orderline;
            el_node.addEventListener('click', this.line_click_handler);
            var el_lot_icon = el_node.querySelector('.line-lot-icon');
            if (el_lot_icon) {
                el_lot_icon.addEventListener('click', (function () {
                    this.show_product_lot(orderline);
                }.bind(this)));
            }

            orderline.node = el_node;
            return el_node;
        }
    })

});