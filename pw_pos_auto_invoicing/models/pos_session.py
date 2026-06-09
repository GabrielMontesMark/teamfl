# -*- coding: utf-8 -*-
from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_pos_config(self):
        result = super()._loader_params_pos_config()
        if 'search_params' in result and 'fields' in result['search_params']:
            result['search_params']['fields'].append('is_auto_invoice')
        return result
