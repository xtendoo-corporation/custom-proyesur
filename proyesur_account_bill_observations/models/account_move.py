from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    observaciones = fields.Text(
        string="Observaciones",
        help="Observaciones internas para facturas y abonos de proveedor.",
    )

