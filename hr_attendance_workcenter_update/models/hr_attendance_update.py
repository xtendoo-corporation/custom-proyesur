from odoo import models, fields, api
import csv
import base64
from io import StringIO

class HrAttendanceWorkcenterUpdate(models.TransientModel):
    _name = 'hr.attendance.workcenter.update'
    _description = 'Actualizar Work Center desde CSV'

    file = fields.Binary(string='Archivo CSV', required=True)
    filename = fields.Char(string='Nombre del archivo')

    def action_update_workcenter(self):
        if not self.file:
            return

        data = base64.b64decode(self.file)
        csvfile = StringIO(data.decode('utf-8'))
        reader = csv.DictReader(csvfile)

        updated = 0
        for row in reader:
            record_id = int(row.get('id', 0))
            work_center_id = row.get('work_center_id')
            if not record_id or not work_center_id:
                continue

            attendance = self.env['hr.attendance'].search([('id', '=', record_id)], limit=1)
            if attendance:
                attendance.work_center_id = int(work_center_id)
                updated += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Actualización completada',
                'message': f'Se actualizaron {updated} registros',
                'type': 'success',
                'sticky': False,
            }
        }
