# -*- coding: utf-8 -*-
{
    'name'          : "Twelve Month Report",
    'category'      : 'Inventroy',
    'version'       : '12.0.1.0',
    'author'        : "Aung Myo Swe",
    'website'       : "www.asiamatrixsoftware.com",
    'email'         :'aungmyoswe@asiamatrixsoftware.com',
    'summary'       : """Report Inventroy Out Data For Twelve Month""",
    'description'   : """
    ###################
    Twelve Month Report
    ###################
    This module is to seen the whole data from warehouse for twelve report.""",
    'depends'       : ['stock'],
    'data': ['wizards/twelve_month_report.xml'],
    'images'        :['static/src/img/icon.png'],
    'application'   :True,
    'auto_install'  :False,
    'installable'   :True,

}