{
    "name": "Sale Order Report Proyesur",
    "summary": "Mejora la impresión PDF de presupuestos permitiendo el corte correcto de textos largos entre páginas",
    "version": "18.0.1.0.0",
    "description": """
        Hereda el template de impresión de presupuestos de venta para aplicar
        estilos CSS que permiten a wkhtmltopdf partir correctamente las filas
        con descripciones largas entre páginas del PDF.
    """,
    "author": "Xtendoo",
    "company": "Xtendoo",
    "website": "https://xtendoo.es",
    "category": "Sales",
    "license": "AGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        "views/report_saleorder_proyesur.xml",
    ],
    "installable": True,
    "auto_install": False,
}

