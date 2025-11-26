# Copyright 2023 Camilo <Xtendoo, https://xtendoo.es/>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


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
            if not vals.get('employee_timesheet_cost'):
                if vals.get('employee_id'):
                    # Si tiene empleado, usar su hourly_cost
                    employee = self.env['hr.employee'].browse(vals['employee_id'])
                    vals['employee_timesheet_cost'] = employee.hourly_cost or 4.38
                elif vals.get('project_id'):
                    # Si no tiene empleado pero tiene proyecto, usar 4.38 por defecto
                    vals['employee_timesheet_cost'] = 4.38
        return super().create(vals_list)

    def write(self, vals):
        # Si se asigna empleado y no hay coste fijado, asignar el coste del empleado
        if vals.get('employee_id'):
            for rec in self:
                if not rec.employee_timesheet_cost or rec.employee_timesheet_cost == 0.0:
                    employee = self.env['hr.employee'].browse(vals['employee_id'])
                    if 'employee_timesheet_cost' not in vals:
                        vals['employee_timesheet_cost'] = employee.hourly_cost or 4.38
        # Si se asigna proyecto sin empleado y sin coste, usar 4.38 por defecto
        elif vals.get('project_id'):
            for rec in self:
                if not rec.employee_id and (not rec.employee_timesheet_cost or rec.employee_timesheet_cost == 0.0):
                    if 'employee_timesheet_cost' not in vals:
                        vals['employee_timesheet_cost'] = 4.38
        return super().write(vals)

    @api.depends('unit_amount', 'employee_timesheet_cost')
    def _compute_employee_timesheet_cost_total(self):
        for line in self:
            line.employee_timesheet_cost_total = line.unit_amount * line.employee_timesheet_cost

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for line in self:
            if line.employee_id:
                line.employee_timesheet_cost = line.employee_id.hourly_cost or 4.38
            elif line.project_id:
                # Si no hay empleado pero hay proyecto, usar 4.38 por defecto
                line.employee_timesheet_cost = 4.38

    @api.onchange('project_id')
    def _onchange_project_id(self):
        for line in self:
            # Si se selecciona un proyecto y no hay empleado ni coste, asignar 4.38
            if line.project_id and not line.employee_id and not line.employee_timesheet_cost:
                line.employee_timesheet_cost = 4.38
