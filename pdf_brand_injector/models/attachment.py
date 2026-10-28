import base64
import fitz  # PyMuPDF
from odoo import models

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def create(self, vals):
        record = super().create(vals)

        if record.mimetype == 'application/pdf' and record.datas:
            try:
                pdf_data = base64.b64decode(record.datas)
                pdf = fitz.open(stream=pdf_data, filetype="pdf")

                company = record.env.company
                logo = company.logo

                if logo:
                    logo_data = base64.b64decode(logo)

                    config = record.env['ir.config_parameter'].sudo()

                    # 🔹 get values
                    position = config.get_param('auto_logo_pdf.logo_position', 'top_left')
                    x = int(config.get_param('auto_logo_pdf.logo_x', 50))
                    y = int(config.get_param('auto_logo_pdf.logo_y', 50))
                    w = int(config.get_param('auto_logo_pdf.logo_width', 100))
                    h = int(config.get_param('auto_logo_pdf.logo_height', 50))

                    for page in pdf:
                        page_width = page.rect.width
                        page_height = page.rect.height

                        # 🔥 USE DROPDOWN if X/Y not changed
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

                        # 🔹 insert image
                        rect = fitz.Rect(x, y, x + w, y + h)
                        page.insert_image(rect, stream=logo_data)

                    new_pdf = pdf.tobytes()
                    pdf.close()

                    record.datas = base64.b64encode(new_pdf)

            except Exception as e:
                print("Error:", e)

        return record