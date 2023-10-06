{
    "name": "Document Format Proyesur",
    "summary": """Formatos de documentos de Proyesur""",
    "version": "15.0.1.0.0",
    "description": """Formatos de documentos de Proyesur""",
    "author": "Jaime Millán",
    "company": "Xtendoo",
    "website": "https://xtendoo.es",
    "category": "Extra Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "web"
    ],
    "data": [
        "views/paper_format.xml",
        "views/invoice/report_invoice_document.xml",
        #Brico
        "views/brico/layout/brico_layout_clean.xml",
        "views/brico/sale_order/report_sale_document.xml",
        "views/brico/layout/brico_layout_clean_invoice.xml",
        "views/brico/invoice/report_invoice_document.xml",
        "views/brico/delivery/report_delivery_document.xml"
    ],
    "installable": True,
    "auto_install": False,
}
