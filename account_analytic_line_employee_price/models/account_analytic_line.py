# Copyright 2023 Camilo <Xtendoo, https://xtendoo.es/>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'


    def _compute_employee_timesheet_cost_total(self):
        for line in self:
            if line.employee_timesheet_cost == 0.0:
                line.employee_timesheet_cost = line.employee_id.timesheet_cost
            line.employee_timesheet_cost_total = line.unit_amount * line.employee_timesheet_cost

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for line in self:
            line.employee_timesheet_cost = line.employee_id.timesheet_cost

    employee_timesheet_cost = fields.Monetary(
        string="Employee timesheet cost",
        groups="hr.group_hr_user",
        default=lambda self: self._get_default_employee_timesheet_cost(),
    )

    @api.model
    def _get_default_employee_timesheet_cost(self):
        print("*" * 100)
        print("line.employee_id", self.employee_id)
        print("line.employee_id.timesheet_cost", self.employee_id.timesheet_cost)
        print("*" * 100)
        return self.employee_id.timesheet_cost

    employee_timesheet_cost_total = fields.Monetary(
        string="Employee timesheet cost total",
        compute='_compute_employee_timesheet_cost_total',
        groups="hr.group_hr_user",
        readonly=True,
    )
