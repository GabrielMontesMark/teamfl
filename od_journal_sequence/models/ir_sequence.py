# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = "ir.sequence"

    sar = fields.Boolean(string="Secuencia SAR")
    cai = fields.Char(string="Cai")
    fecha_desde = fields.Date(string="Fecha inicial de emision")
    fecha_hasta = fields.Date(string="Fecha limite emision")
    
    correlativo_desde = fields.Char(string="Rango inicial autorizado", compute="_range_cai")
    numero_correlativo_desde = fields.Integer(string="Numero rango inicial", help="solo utilizar el numero")
    correlativo_hasta = fields.Char(string="Rango final autorizado", compute="_range_cai")
    numero_correlativo_hasta = fields.Integer(string="Numero rango final", help="solo utilizar el numero")

    @api.depends("prefix", "numero_correlativo_desde", "numero_correlativo_hasta", "padding")
    def _range_cai(self):
        for move in self:
            move.correlativo_desde = False
            move.correlativo_hasta = False
            if move.numero_correlativo_desde:
                prefix = move.prefix or ""
                move.correlativo_desde = str(prefix + str(move.numero_correlativo_desde).zfill(move.padding or 4))
            if move.numero_correlativo_hasta:
                prefix = move.prefix or ""
                move.correlativo_hasta = str(prefix + str(move.numero_correlativo_hasta).zfill(move.padding or 4))