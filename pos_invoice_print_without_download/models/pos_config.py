# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import fields, models, api
import logging
import base64
_logger = logging.getLogger(__name__)

class PosConfig(models.Model):
    _inherit = 'pos.config'

    invoice_print = fields.Boolean(string="Print Invoice Without its Download", help="Enable this options to Print Invoice Without Download .", default=True)
    
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    pos_invoice_print = fields.Boolean(related='pos_config_id.invoice_print',readonly=False)

class PosOrder(models.Model):
    _inherit = "pos.order" 

    @api.model
    def action_invoice_pdf(self,invoice_id):
        _logger.info(f"\n\n\n{invoice_id}\n\n\n")
        pdf =  self.env['ir.actions.report']._render_qweb_pdf("account.account_invoices",[invoice_id])[0]
        base = base64.b64encode(pdf).decode('utf-8')
        return base
        
    def action_receipt_to_invoice(self, *args, **kwargs):
        res = super().action_receipt_to_invoice(*args, **kwargs)
        # If the option to prevent download is enabled, we intercept the ir.actions.report
        # dictionary that tells the frontend to download the PDF, and return False instead.
        if self.config_id.invoice_print and isinstance(res, dict) and res.get('type') == 'ir.actions.report':
            _logger.info("POS Invoice Print Without Download: Intercepted backend action to prevent automatic download.")
            return False
        return res
        
        