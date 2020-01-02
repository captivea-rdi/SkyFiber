# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    agent_id = fields.Many2one("res.partner", domain=[("is_agent", "=", True)])
    order_id = fields.Many2one("sale.order", string="Sale Order")
    total_commission = fields.Monetary(
        "Total Commission",
        store=True,
        readonly=True,
        compute="_compute_total_commission",
    )

    @api.depends("invoice_line_ids.commission_amount")
    def _compute_total_commission(self):
        for order in self:
            commission_totals = order.invoice_line_ids.mapped(
                lambda line: line.commission_amount
            )
            order.total_commission = sum(commission_totals)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    commission_percent = fields.Integer(string="Commission %", default=0)
    commission_amount = fields.Monetary(
        string="Commission Value", readonly=True, compute="_compute_commission_amount"
    )

    @api.depends("price_subtotal", "commission_percent")
    def _compute_commission_amount(self):
        for line in self:
            line.commission_amount = (line.price_subtotal * line.commission_percent) / 100.0
