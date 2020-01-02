# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    agent_id = fields.Many2one("res.partner", domain=[("is_agent", "=", True)])

    def _prepare_invoice_data(self):
        res = super(SaleSubscription, self)._prepare_invoice_data()
        res.update(agent_id=self.agent_id.id)
        return res

    def _prepare_invoice_line(self, line, fiscal_position):
        res = super(SaleSubscription, self)._prepare_invoice_line(line, fiscal_position)
        res.update(commission_percent=line.commission_percent)
        return res


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    commission_percent = fields.Integer(string="Commission %", default=0)
    commission_amount = fields.Float(
        string="Commission Value", readonly=True, compute="_compute_commission_amount"
    )

    @api.depends("price_subtotal", "commission_percent")
    def _compute_commission_amount(self):
        for line in self:
            line.commission_amount = (line.price_subtotal * line.commission_percent) / 100.0
