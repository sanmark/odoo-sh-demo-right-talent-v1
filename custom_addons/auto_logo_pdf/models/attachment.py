import fitz  # PyMuPDF

from odoo import api, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)

    def write(self, vals):
        if 'raw' in vals and vals['raw']:
            raw_value = vals['raw']

            if hasattr(raw_value, 'content'):
                pdf_data = raw_value.content
            else:
                pdf_data = raw_value

            if pdf_data:
                try:
                    pdf = fitz.open(
                        stream=pdf_data,
                        filetype="pdf",
                    )

                    for record in self:
                        company = record.env.company
                        logo = company.logo

                        if not logo:
                            continue

                        logo_data = logo.content

                        config = record.env[
                            'ir.config_parameter'
                        ].sudo()

                        position = config.get_str(
                            'auto_logo_pdf.logo_position',
                            default='top_left',
                        )
                        x = config.get_int(
                            'auto_logo_pdf.logo_x',
                            default=50,
                        )
                        y = config.get_int(
                            'auto_logo_pdf.logo_y',
                            default=50,
                        )
                        w = config.get_int(
                            'auto_logo_pdf.logo_width',
                            default=100,
                        )
                        h = config.get_int(
                            'auto_logo_pdf.logo_height',
                            default=50,
                        )

                        for page in pdf:
                            page_width = page.rect.width
                            page_height = page.rect.height

                            logo_x = x
                            logo_y = y

                            if x == 50 and y == 50:
                                if position == 'top_left':
                                    logo_x, logo_y = 20, 20

                                elif position == 'top_center':
                                    logo_x = (page_width - w) / 2
                                    logo_y = 20

                                elif position == 'top_right':
                                    logo_x = page_width - w - 20
                                    logo_y = 20

                                elif position == 'middle_center':
                                    logo_x = (page_width - w) / 2
                                    logo_y = (page_height - h) / 2

                                elif position == 'bottom_center':
                                    logo_x = (page_width - w) / 2
                                    logo_y = page_height - h - 20

                                elif position == 'bottom_right':
                                    logo_x = page_width - w - 20
                                    logo_y = page_height - h - 20

                            rect = fitz.Rect(
                                logo_x,
                                logo_y,
                                logo_x + w,
                                logo_y + h,
                            )

                            page.insert_image(
                                rect,
                                stream=logo_data,
                            )

                    vals['raw'] = pdf.tobytes()
                    pdf.close()

                except Exception as e:
                    print("Error injecting logo into PDF:", e)

        return super().write(vals)