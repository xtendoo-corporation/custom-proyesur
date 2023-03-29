# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Analytic Line Employee Price",
    "version": "15.0.1.0.2",
    "category": "Generic Modules/Analytic",
    "development_status": "Production/Stable",
    "author": "Camilo <Xtendoo>",
    "summary": "Account analytic line employee price",
    "website": "https://github.com/OCA/account-payment",
    "license": "AGPL-3",
    "depends": [
        "account",
        "hr",
        "hr_timesheet_sheet"
    ],
    "data": [
        "views/analytic_account_line_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
