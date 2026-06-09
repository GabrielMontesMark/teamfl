#  -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################

from . import models
import warnings

def pre_init_check(cr):
    from odoo.service import common
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if server_serie!='17.0':
        warnings.warn(f"Module support Odoo series 17.0 found {server_serie}.")
    return True    