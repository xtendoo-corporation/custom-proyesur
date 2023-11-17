# Copyright 2023 Camilo <Xtendoo, https://xtendoo.es/>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, tools


def pre_init_hook(cr):
    logger = logging.getLogger(__name__)
    logger.info(
        "Update value employee_timesheet_cost with value timesheet_cost from employee_id"
    )
    cr.execute(
        """ ALTER TABLE account_analytic_line ADD COLUMN employee_timesheet_cost FLOAT;
     """
    )
    cr.execute(
        """ UPDATE account_analytic_line SET employee_timesheet_cost = emp.timesheet_cost
        FROM account_analytic_line aal
        INNER JOIN hr_employee emp ON emp.id = aal.employee_id
        WHERE aal.employee_id IS NOT NULL;
     """
    )
    logger.info(
        "Finished update account_move_line.employee_timesheet_cost column"
    )
