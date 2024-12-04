from odoo import models, fields, api, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    tiene_retenciones = fields.Boolean(string="Tiene Retenciones", compute='_compute_tiene_retenciones', store=False)

    @api.depends('order_line.taxes_id')
    def _compute_tiene_retenciones(self):
        for order in self:
            tiene_retenciones = False

            for line in order.order_line:
                for tax in line.taxes_id:
                    if tax.name.startswith("Retenciones"):
                        tiene_retenciones = True
                        break
                if tiene_retenciones:
                    break

            order.tiene_retenciones = tiene_retenciones
            print("Tiene retenciones ", tiene_retenciones)
