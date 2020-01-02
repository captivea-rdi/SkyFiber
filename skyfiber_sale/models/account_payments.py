# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def action_validate_invoice_payment(self):
        """
        # NOTE: The usecase for this dev has only one subscription per SO, so we don't
        # attempt to map invoices to subscriptions. Instead, we just set the start date
        # for the first subscription we find.s
        """
        res = super(AccountPayment, self).action_validate_invoice_payment()
        ctx = self.env.context
        if (
            res
            and ctx.get("active_id")
            and ctx.get("active_model") == "account.invoice"
        ):
            order = self.env["account.invoice"].browse(ctx.get("active_id")).order_id
            if order and order.subscription_count > 0:
                # Set start date only to first subscription
                for line in order.order_line:
                    if line.subscription_id:
                        line.subscription_id.date_start = self.payment_date
                        break
        return res
