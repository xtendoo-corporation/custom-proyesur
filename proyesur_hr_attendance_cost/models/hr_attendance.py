import pytz

from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    cost_date = fields.Date(
        string="Fecha de coste",
        compute="_compute_cost_date",
        store=True,
        index=True,
    )
    # Redefine el campo de hr_attendance_work_center, que solo se rellenaba
    # con un onchange del formulario y quedaba a 0 en el resto de casos.
    coste_total = fields.Float(
        compute="_compute_coste_total",
        store=True,
        readonly=True,
    )
    daily_cost = fields.Float(
        string="Coste del día",
        compute="_compute_daily_cost",
        help="Coste total del trabajador en el día de esta asistencia "
        "(suma de coste/hora x horas trabajadas de todas sus asistencias "
        "de ese día).",
    )

    @api.depends("check_in", "employee_id.tz")
    def _compute_cost_date(self):
        for att in self:
            if not att.check_in:
                att.cost_date = False
                continue
            tz = pytz.timezone(att.employee_id.tz or self.env.user.tz or "UTC")
            att.cost_date = pytz.utc.localize(att.check_in).astimezone(tz).date()

    @api.depends("coste", "worked_hours")
    def _compute_coste_total(self):
        for att in self:
            att.coste_total = att.coste * att.worked_hours

    @api.depends("coste", "worked_hours", "cost_date", "employee_id")
    def _compute_daily_cost(self):
        self.env["hr.attendance"].flush_model(
            ["coste", "worked_hours", "cost_date", "employee_id"]
        )
        rows = self.env["hr.attendance"].sudo().search_read(
            [
                ("employee_id", "in", self.employee_id.ids),
                ("cost_date", "in", [d for d in self.mapped("cost_date") if d]),
            ],
            ["employee_id", "cost_date", "coste", "worked_hours"],
        )
        totals = {}
        for row in rows:
            key = (row["employee_id"][0], row["cost_date"])
            totals[key] = totals.get(key, 0.0) + row["coste"] * row["worked_hours"]
        for att in self:
            att.daily_cost = totals.get((att.employee_id.id, att.cost_date), 0.0)
