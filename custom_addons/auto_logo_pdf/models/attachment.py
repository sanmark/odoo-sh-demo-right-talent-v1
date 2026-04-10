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

                company = self.env.company
                logo = company.logo

                if logo:
                    logo_data = base64.b64decode(logo)

                    for page in pdf:
                        config = record.env['ir.config_parameter'].sudo()

                        x = int(config.get_param('auto_logo_pdf.logo_x', 50))
                        y = int(config.get_param('auto_logo_pdf.logo_y', 50))
                        w = int(config.get_param('auto_logo_pdf.logo_width', 100))
                        h = int(config.get_param('auto_logo_pdf.logo_height', 50))

                        rect = fitz.Rect(x, y, x + w, y + h)
                        page.insert_image(rect, stream=logo_data)

                    new_pdf = pdf.tobytes()
                    pdf.close()
                    
                    record.datas = base64.b64encode(new_pdf)

            except Exception as e:
                print("Error:", e)

        return record