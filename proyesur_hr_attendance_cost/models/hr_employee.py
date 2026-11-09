from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    cost_per_day = fields.Monetary(
        string="Coste/día",
        currency_field="currency_id",
        groups="hr.group_hr_user",
        help="Coste fijo diario del trabajador.",
    )
