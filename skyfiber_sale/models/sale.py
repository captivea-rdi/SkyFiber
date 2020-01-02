# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    agent_id = fields.Many2one("res.partner", domain=[("is_agent", "=", True)])
    total_commission = fields.Monetary(
        string="Total Commission",
        store=True,
        readonly=True,
        compute="_compute_total_commission",
    )

    @api.depends("order_line.commission_amount")
    def _compute_total_commission(self):
        for order in self:
            commission_totals = order.order_line.mapped("commission_amount")
            order.total_commission = sum(commission_totals)

    def _prepare_subscription_data(self, template):
        res = super(SaleOrder, self)._prepare_subscription_data(template)
        res.update(agent_id=self.agent_id.id or False)
        return res

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update(order_id=self.id, agent_id=self.agent_id.id or False)
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commission_percent = fields.Integer(
        string="Commission %",
        default=0,
        states={
            "sale": [("readonly", True)],
            "done": [("readonly", True)],
            "cancel": [("readonly", True)],
        },
    )
    commission_amount = fields.Monetary(
        string="Commission Value", readonly=True, compute="_compute_commission_amount"
    )

    @api.depends("price_subtotal", "commission_percent")
    def _compute_commission_amount(self):
        for line in self:
            line.commission_amount = (line.price_subtotal * line.commission_percent) / 100.0

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update(commission_percent=self.commission_percent)
        return res

    def _prepare_subscription_line_data(self):
        res = super(SaleOrderLine, self)._prepare_subscription_line_data()
        # There's the unlikely possiblilty that the order of commands doesn't match the
        # lines. It's unlikely because recordsets are ordered, and the commands are
        # created by iterating through the lines recordset. But if it's observed later
        # that commission values are applied to the wrong lines, this is where checks
        # can be done to match commands with the correct order lines.
        for line, cmd in zip(self, res):
            cmd[2].update(commission_percent=line.commission_percent)
        return res
