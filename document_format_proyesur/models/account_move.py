from odoo import models, fields, api, _
from collections import defaultdict
from odoo.tools.misc import formatLang, format_date, get_lang, groupby

class AccountMove(models.Model):
    _inherit = 'account.move'

    tiene_retenciones = fields.Boolean(string="Tiene Retenciones", compute='_compute_tiene_retenciones', store=False)

    @api.depends('invoice_line_ids.tax_ids')
    def _compute_tiene_retenciones(self):
        for move in self:
            tiene_retenciones = False

            for line in move.invoice_line_ids:
                for tax in line.tax_ids:
                    if tax.name.startswith("Retenciones"):
                        tiene_retenciones = True
                        break
                if tiene_retenciones:
                    break

            move.tiene_retenciones = tiene_retenciones
            print("Tiene retenciones ", tiene_retenciones)

    @api.model
    def _get_tax_totals(self, partner, tax_lines_data, amount_total, amount_untaxed, currency):
        self._compute_tiene_retenciones()
        """ Compute the tax totals for the provided data.

        :param partner:        The partner to compute totals for
        :param tax_lines_data: All the data about the base and tax lines as a list of dictionaries.
        :param amount_total:   Total amount, with taxes.
        :param amount_untaxed: Total amount without taxes.
        :param currency:       The currency in which the amounts are computed.

        :return: A dictionary in the following form:
            {
                'amount_total':                              The total amount to be displayed on the document, including every total types.
                'amount_untaxed':                            The untaxed amount to be displayed on the document.
                'formatted_amount_total':                    Same as amount_total, but as a string formatted accordingly with partner's locale.
                'formatted_amount_untaxed':                  Same as amount_untaxed, but as a string formatted accordingly with partner's locale.
                'total_without_retention':                   Total amount without retention formatted as a string.
                'allow_tax_edition':                         True if the user should have the ability to manually edit the tax amounts by group to fix rounding errors.
                'groups_by_subtotals':                       A dictionary formed liked {'subtotal': groups_data}
                'subtotals':                                 A list of dictionaries in the following form.
            }
        """
        account_tax = self.env['account.tax']

        grouped_taxes = defaultdict(
            lambda: defaultdict(lambda: {'base_amount': 0.0, 'tax_amount': 0.0, 'base_line_keys': set()}))
        subtotal_priorities = {}
        total_retention = 0.0

        print("Tax lines data:", tax_lines_data)

        for line_data in tax_lines_data:
            print("Line data:", line_data)
            tax_group = line_data['tax'].tax_group_id

            # Update subtotals priorities
            if tax_group.preceding_subtotal:
                subtotal_title = tax_group.preceding_subtotal
                new_priority = tax_group.sequence
            else:
                subtotal_title = _("Untaxed Amount")
                new_priority = 0

            if subtotal_title not in subtotal_priorities or new_priority < subtotal_priorities[subtotal_title]:
                subtotal_priorities[subtotal_title] = new_priority

            # Update tax data
            tax_group_vals = grouped_taxes[subtotal_title][tax_group]

            if 'base_amount' in line_data:
                if tax_group == line_data.get('tax_affecting_base', account_tax).tax_group_id:
                    continue

                if line_data['line_key'] not in tax_group_vals['base_line_keys']:
                    tax_group_vals['base_line_keys'].add(line_data['line_key'])
                    tax_group_vals['base_amount'] += line_data['base_amount']

            else:
                tax_group_vals['tax_amount'] += line_data['tax_amount']

                print("Tax group name:", tax_group.name)
                # Suma las retenciones si el nombre del grupo de impuestos comienza con "Retenciones"
                if tax_group.name.startswith("Retenciones"):
                    total_retention += line_data['tax_amount']  # Almacena como float

        # Compute groups_by_subtotal
        groups_by_subtotal = {}
        for subtotal_title, groups in grouped_taxes.items():
            groups_vals = [{
                'tax_group_name': group.name,
                'tax_group_amount': amounts['tax_amount'],
                'tax_group_base_amount': amounts['base_amount'],
                'formatted_tax_group_amount': formatLang(self.env, amounts['tax_amount'], currency_obj=currency),
                'formatted_tax_group_base_amount': formatLang(self.env, amounts['base_amount'], currency_obj=currency),
                'tax_group_id': group.id,
                'group_key': '%s-%s' % (subtotal_title, group.id),
            } for group, amounts in sorted(groups.items(), key=lambda l: l[0].sequence)]

            groups_by_subtotal[subtotal_title] = groups_vals

        # Compute subtotals
        subtotals_list = []
        previous_subtotals_tax_amount = 0
        for subtotal_title in sorted((sub for sub in subtotal_priorities), key=lambda x: subtotal_priorities[x]):
            subtotal_value = amount_untaxed + previous_subtotals_tax_amount
            subtotals_list.append({
                'name': subtotal_title,
                'amount': subtotal_value,
                'formatted_amount': formatLang(self.env, subtotal_value, currency_obj=currency),
            })

            subtotal_tax_amount = sum(group_val['tax_group_amount'] for group_val in groups_by_subtotal[subtotal_title])
            previous_subtotals_tax_amount += subtotal_tax_amount

        print("Total retention ",total_retention)
        # Formatear la cantidad de retenciones

        # Calcular el total sin retenciones
        total_without_retention = amount_total - total_retention
        print("total_without_retention ", total_without_retention)
        # Formatear el total sin retenciones
        formatted_total_without_retention = formatLang(self.env, total_without_retention, currency_obj=currency)
        print("formatted_total_without_retention ", formatted_total_without_retention)
        # Assign json-formatted result to the field
        return {
            'amount_total': amount_total,
            'amount_untaxed': amount_untaxed,
            'formatted_amount_total': formatLang(self.env, amount_total, currency_obj=currency),
            'formatted_amount_untaxed': formatLang(self.env, amount_untaxed, currency_obj=currency),
            'total_without_retention': formatted_total_without_retention,  # Total sin retenciones
            'groups_by_subtotal': groups_by_subtotal,
            'subtotals': subtotals_list,
            'allow_tax_edition': False,
        }
