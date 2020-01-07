# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def post(self):
        """
        # NOTE: The usecase for this dev has only one subscription per SO, so we don't
        # attempt to map move to subscriptions. Instead, we just set the start date
        # for the first subscription we find.s
        """
        res = super(AccountPayment, self).post()
        ctx = self.env.context
        if (
            res
            and ctx.get("active_id")
            and ctx.get("active_model") == "account.move"
        ):
            order = self.env["account.move"].browse(ctx.get("active_id")).order_id
            if order and order.subscription_count > 0:
                # Set start date only to first subscription
                for line in order.order_line:
                    if line.subscription_id:
                        line.subscription_id.date_start = self.payment_date
                        break
        return res
