# Copyright 2023 Camilo <Xtendoo, https://xtendoo.es/>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _compute_employee_timesheet_cost_total(self):
        for line in self:
            line.employee_timesheet_cost_total = line.unit_amount * line.employee_timesheet_cost

    employee_timesheet_cost = fields.Monetary(
        string="Employee timesheet cost",
        related="employee_id.timesheet_cost",
        currency_field='currency_id',
        groups="hr.group_hr_user",
    )

    employee_timesheet_cost_total = fields.Monetary(
        string="Employee timesheet cost total",
        compute='_compute_employee_timesheet_cost_total',
        currency_field='currency_id',
        groups="hr.group_hr_user",
    )

    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True
    )



