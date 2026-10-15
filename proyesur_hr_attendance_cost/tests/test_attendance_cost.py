from datetime import datetime

from odoo.tests.common import TransactionCase


class TestAttendanceCost(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env["hr.employee"].create(
            {"name": "Test", "hourly_cost": 10.0, "tz": "UTC"}
        )
        cls.center = cls.env["res.partner"].create(
            {"name": "Centro", "is_work_center": True}
        )

    def _att(self, day, h_in, h_out):
        return self.env["hr.attendance"].create(
            {
                "employee_id": self.employee.id,
                "work_center_id": self.center.id,
                "check_in": datetime(2026, 1, day, h_in),
                "check_out": datetime(2026, 1, day, h_out),
            }
        )

    def test_daily_cost_shared_by_all_attendances_of_the_day(self):
        a1 = self._att(5, 8, 12)  # 4h
        a2 = self._att(5, 14, 16)  # 2h
        other_day = self._att(6, 8, 10)  # 2h
        self.assertEqual(a1.coste_total, 40.0)
        self.assertEqual(a2.coste_total, 20.0)
        self.assertEqual(a1.daily_cost, 60.0)
        self.assertEqual(a2.daily_cost, 60.0)
        self.assertEqual(other_day.daily_cost, 20.0)

    def test_checkout_change_recomputes(self):
        a1 = self._att(5, 8, 12)
        a1.check_out = datetime(2026, 1, 5, 14)  # 6h menos 1h de comida
        self.assertEqual(a1.coste_total, 50.0)
        self.assertEqual(a1.daily_cost, 50.0)

    def test_old_cost_kept_when_employee_cost_changes(self):
        a1 = self._att(5, 8, 12)
        self.employee.hourly_cost = 20.0
        self.assertEqual(a1.coste, 10.0)
        self.assertEqual(a1.daily_cost, 40.0)

    def test_open_attendance_costs_on_checkout(self):
        att = self.env["hr.attendance"].create(
            {
                "employee_id": self.employee.id,
                "work_center_id": self.center.id,
                "check_in": datetime(2026, 1, 5, 8),
            }
        )
        self.assertEqual(att.coste_total, 0.0)
        att.write({"check_out": datetime(2026, 1, 5, 12)})
        self.assertEqual(att.coste_total, 40.0)
