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
                        rect = fitz.Rect(50, 50, 150, 100)
                        page.insert_image(rect, stream=logo_data)

                    new_pdf = pdf.tobytes()
                    record.datas = base64.b64encode(new_pdf)

            except Exception as e:
                print("Error:", e)

        return record