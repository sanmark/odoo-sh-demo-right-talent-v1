import base64

import fitz  # PyMuPDF

from odoo import api, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            if record.mimetype != 'application/pdf' or not record.datas:
                continue

            try:
                pdf_data = record.datas.content
                pdf = fitz.open(stream=pdf_data, filetype="pdf")

                company = record.env.company
                logo = company.logo

                if logo:
                    logo_data = logo.content

                    config = record.env['ir.config_parameter'].sudo()

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

                        if x == 50 and y == 50:
                            if position == 'top_left':
                                x, y = 20, 20

                            elif position == 'top_center':
                                x = (page_width - w) / 2
                                y = 20

                            elif position == 'top_right':
                                x = page_width - w - 20
                                y = 20

                            elif position == 'middle_center':
                                x = (page_width - w) / 2
                                y = (page_height - h) / 2

                            elif position == 'bottom_center':
                                x = (page_width - w) / 2
                                y = page_height - h - 20

                            elif position == 'bottom_right':
                                x = page_width - w - 20
                                y = page_height - h - 20

                        rect = fitz.Rect(x, y, x + w, y + h)
                        page.insert_image(rect, stream=logo_data)

                    new_pdf = pdf.tobytes()
                    pdf.close()

                    record.write({
                        'datas': base64.b64encode(new_pdf),
                    })

            except Exception as e:
                print("Error:", e)

        return records
