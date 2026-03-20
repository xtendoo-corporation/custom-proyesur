{
    'name': 'HR Attendance Work Center Update',
    'version': '1.0',
    'summary': 'Actualizar work_center_id de hr_attendance desde CSV',
    'description': 'Permite importar un CSV para actualizar work_center_id de asistencias línea por línea.',
    'category': 'Human Resources',
    'author': 'Dani Dominguez',
    'depends': ['hr', 'hr_attendance'],
    'data': [
        'views/hr_attendance_update_views.xml',
    ],
    'installable': True,
    'application': False,
}
