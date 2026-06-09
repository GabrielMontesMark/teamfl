# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    name = fields.Char(string='Number', copy=False, compute="_compute_name_by_sequence", readonly=False, store=True, index=True, tracking=True)
    cai = fields.Char(string="CAI", compute="_compute_sar", store=True)
    fecha_desde = fields.Date(string="Fecha Desde", compute="_compute_sar", store=True)
    fecha_hasta = fields.Date(string="Fecha Hasta", compute="_compute_sar", store=True)
    correlativo_desde = fields.Char(string="Correlativo Desde", compute="_compute_sar", store=True)
    correlativo_hasta = fields.Char(string="Correlativo Hasta", compute="_compute_sar", store=True)
    #const_reg_exo = fields.Char(string="Const. Reg. Exo.", states={'posted': [('readonly', True)]})
    #compra_exenta = fields.Char(string="Compra Exenta", states={'posted': [('readonly', True)]})
    #reg_sag = fields.Char(string="Reg. SAG", states={'posted': [('readonly', True)]})

    def _compute_amount2words_signed(self):
        for rec in self:
                rec.amount_words_signed = str(rec.company_id.currency_id.amount_to_text(rec.amount_total_signed))
    
    amount_words_signed = fields.Char(string="Monto en letras: ", help=
        "Autogenerado por el sistema", compute='_compute_amount2words_signed')

    @api.depends("state", "journal_id", "date")
    def _compute_name_by_sequence(self):
        for move in self:
            name = move.name or "/"
            if (
                    move.state == "posted"
                    and (not move.name or move.name == "/")
                    and move.journal_id
                    and move.journal_id.sequence_id
            ):
                if (
                        move.move_type in ("out_refund", "in_refund")
                        and move.journal_id.type in ("sale", "purchase")
                        and move.journal_id.refund_sequence
                        and move.journal_id.refund_sequence_id
                ):
                    seq = move.journal_id.refund_sequence_id
                else:
                    seq = move.journal_id.sequence_id
                name = seq.next_by_id(sequence_date=move.date)
            move.name = name

            if move.journal_id.sequence_id.sar == True:
                if move.journal_id.sequence_id.fecha_hasta:
                    if move.journal_id.sequence_id.fecha_hasta <= date.today():
                        raise ValidationError(_('No se puede crear documento a mayor rango'))
                if move.journal_id.sequence_id.numero_correlativo_hasta:
                    if move.journal_id.sequence_id.numero_correlativo_hasta < move.journal_id.sequence_id.number_next_actual:
                        raise ValidationError(_('No se puede crear documento a mayor rango'))

    @api.depends("cai", "journal_id", "journal_id.sequence_id.sar")
    def _compute_sar(self):
        for move in self:
            cai_for = move.cai or ""
            initial_date_cai_for = move.fecha_desde or ""
            limit_date_cai_for = move.fecha_hasta or ""
            initial_range_cai_for = move.correlativo_desde or ""
            final_range_cai_for = move.correlativo_hasta or ""
            if move.journal_id.sequence_id.sar == True:
                if not move.cai:
                    cai_for = move.journal_id.sequence_id.cai
                if not move.fecha_desde:
                    initial_date_cai_for = move.journal_id.sequence_id.fecha_desde
                if not move.fecha_hasta:
                    limit_date_cai_for = move.journal_id.sequence_id.fecha_hasta
                if not move.correlativo_desde:
                    initial_range_cai_for = move.journal_id.sequence_id.correlativo_desde
                if not move.correlativo_hasta:
                    final_range_cai_for = move.journal_id.sequence_id.correlativo_hasta
            else:
                move.cai = cai_for
                move.fecha_desde = initial_date_cai_for
                move.fecha_hasta = limit_date_cai_for
                move.correlativo_desde = initial_range_cai_for
                move.correlativo_hasta = final_range_cai_for

            move.cai = cai_for
            move.fecha_desde = initial_date_cai_for
            move.fecha_hasta = limit_date_cai_for
            move.correlativo_desde = initial_range_cai_for
            move.correlativo_hasta = final_range_cai_for

    def _constrains_date_sequence(self):
        return True

