# Copyright 2023 Camilo <Xtendoo, https://xtendoo.es/>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    employee_timesheet_cost = fields.Monetary(
        string="Employee timesheet cost",
        groups="hr.group_hr_user",
    )

    employee_timesheet_cost_total = fields.Monetary(
        string="Employee timesheet cost total",
        compute='_compute_employee_timesheet_cost_total',
        groups="hr.group_hr_user",
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('employee_id'):
                employee = self.env['hr.employee'].browse(vals['employee_id'])
                vals['employee_timesheet_cost'] = employee.timesheet_cost or 0.0
        return super().create(vals_list)

    def write(self, vals):
        # Si se asigna empleado y se está creando o cambiando el empleado, asignar el coste si no está ya fijado
        if vals.get('employee_id'):
            for rec in self:
                if not rec.employee_timesheet_cost or rec.employee_timesheet_cost == 0.0:
                    employee = self.env['hr.employee'].browse(vals['employee_id'])
                    vals['employee_timesheet_cost'] = employee.timesheet_cost or 0.0
        return super().write(vals)

    @api.depends('unit_amount', 'employee_timesheet_cost')
    def _compute_employee_timesheet_cost_total(self):
        for line in self:
            line.employee_timesheet_cost_total = line.unit_amount * line.employee_timesheet_cost

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for line in self:
            if line.employee_id:
                line.employee_timesheet_cost = line.employee_id.timesheet_cost or 0.0
