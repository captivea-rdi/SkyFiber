# -*- coding: utf-8 -*-
{
    'name': "Sky Fiber: Sale",

    'summary': """
        Sale-related changes for Sky Fiber.""",

    'description': """
        Sale-related changes for Sky Fiber. Includes the following customizations:

Task 1998911:
=============

  a) i) Subscription product is added on SO, customer signs it, technician goes onsite, converts this to Invoice and registers payment. The "Invoice Date" of the first invoice generated from the Sale order should be the start date of the subscription.


b) i) Create a boolean on res.partner to mark a contact as Agent. We can add it below "Is a Customer" field on contact. On Sales quotation and order, we need a field called Agent where we are able to set an agent i.e select from the contacts (Agent=True). This should be added below the customer name (screenshot attached).
   ii) SO line level, we need a new field which captures commission % (default value is 0) and a field which calculates the Commission Value which is (commission % x untaxed amount). As soon as they add a new product - commission column should show 0 - until they edit it. Any user with access to Sales app will set the agent and create SO with commission values.
  iii) Add a "Total Commission" field below the SO total. This is the sum of individual "Commission Values" from SO lines.
See attached screenshot.
   iv) If commission % is edited on sale order line, it should trigger re computation of Commission value. Commission values should not be editable on a confirmed SO, they can edit these on the subscription so that going forward the invoices will have the new commission% and rate.
       A commission would always be created from SO. They will upsell on existing subscription and that would add a new line to the subscription, they will manually add the commission values.

c) i) The "Agent", "Commission %" and "Commission Value" information should flow to the associated Invoice and Subscription. These would be editable on Subscription as needed. If a new agent takes over - they will edit these on Sub so the future invoices will be drives from Subscription line and hence will have the updated commission data.
   ii) All future invoices generated from the subscription should contain this information. Agent field is at the form level and the two commission calculation fields are at the line level.
   iii) We need a total commission Value field on the Invoice below the Total 
We will be using Odoo filters on Invoices to filter down on "Paid" invoices for a duration of time (say 1 month) by an agent to arrive at the total commission $ to be paid.
   iv) If commission % is edited on the subscription line, it should trigger recomputation of Commission value. Future invoices should use this data.
   v) If a new line is added on the invoice (e.g. late fee), its commission value should default to 0. We will not handle invoices marked paid via write-off or credit note.

d) Users with the following access should be able to view and edit "Commission %" and "Commission Value" fields on Invoices and Subscriptions. For other users, these should be invisible.
-> Sales/ Manager
-> Accounting/ Advisor
-> Subscriptions/ Manage Subscriptions
    """,

    'author': "Odoo Inc",
    'website': "http://odoo.com",

    'category': 'Custom Development',
    'version': '0.1',
    'depends': ['account', 'sale_subscription'],

    'data': [
        'views/sale_views.xml',
        'views/partner_views.xml',
        'views/sale_subscription_views.xml',
        'views/account_invoice_view.xml',
    ],
}