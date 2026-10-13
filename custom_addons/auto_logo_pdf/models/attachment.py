
import logging

import fitz

from odoo import api, models

_logger = logging.getLogger(__name__)

MARK = 'auto_logo_pdf'


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        _logger.info(
            "PDF LOGO DEBUG create: ids=%s stream_upload=%s",
            records.ids,
            self.env.context.get('ir_attachment_from_stream'),
        )

        if not self.env.context.get('ir_attachment_from_stream'):
            records._inject_logo_into_pdf()

        return records

    def _upload_file(self, file, create_vals):
        """Inject the logo after Odoo finishes storing an uploaded file."""
        attachment = super()._upload_file(file, create_vals)

        _logger.info(
            "PDF LOGO DEBUG upload_file: id=%s name=%s mimetype=%s",
            attachment.id,
            attachment.name,
            attachment.mimetype,
        )

        attachment._inject_logo_into_pdf()
        return attachment

    def _post_add_create(self, **kwargs):
        _logger.info(
            "PDF LOGO DEBUG post_add_create ENTER: ids=%s",
            self.ids,
        )

        result = super()._post_add_create(**kwargs)

        self._inject_logo_into_pdf()
        return result

    def write(self, vals):
        result = super().write(vals)

        if 'raw' in vals:
            _logger.info(
                "PDF LOGO DEBUG write raw: ids=%s",
                self.ids,
            )
            self._inject_logo_into_pdf()

        return result

    def _inject_logo_into_pdf(self):
        config = self.env['ir.config_parameter'].sudo()

        position = config.get_str(
            'auto_logo_pdf.logo_position',
            default='top_left',
        )
        x = config.get_int('auto_logo_pdf.logo_x', default=50)
        y = config.get_int('auto_logo_pdf.logo_y', default=50)
        width = config.get_int('auto_logo_pdf.logo_width', default=100)
        height = config.get_int('auto_logo_pdf.logo_height', default=50)

        for record in self:
            try:
                if record.mimetype != 'application/pdf':
                    continue

                raw = record.raw
                if not raw or not raw.content:
                    _logger.info(
                        "PDF LOGO DEBUG no content: attachment=%s",
                        record.id,
                    )
                    continue

                logo = record.company_id.logo or record.env.company.logo
                if not logo or not logo.content:
                    _logger.warning(
                        "PDF LOGO DEBUG company logo missing: attachment=%s",
                        record.id,
                    )
                    continue

                pdf = None

                try:
                    pdf = fitz.open(
                        stream=raw.content,
                        filetype='pdf',
                    )

                    meta = {
                        key: value
                        for key, value in (pdf.metadata or {}).items()
                        if key not in ('format', 'encryption') and value
                    }

                    if MARK in (meta.get('keywords') or ''):
                        _logger.info(
                            "PDF LOGO DEBUG already processed: attachment=%s",
                            record.id,
                        )
                        continue

                    for page in pdf:
                        page_width = page.rect.width
                        page_height = page.rect.height

                        logo_x, logo_y = x, y

                        if x == 50 and y == 50:
                            logo_x, logo_y = {
                                'top_left': (20, 20),
                                'top_center': (
                                    (page_width - width) / 2, 20
                                ),
                                'top_right': (
                                    page_width - width - 20, 20
                                ),
                                'middle_center': (
                                    (page_width - width) / 2,
                                    (page_height - height) / 2,
                                ),
                                'bottom_center': (
                                    (page_width - width) / 2,
                                    page_height - height - 20,
                                ),
                                'bottom_right': (
                                    page_width - width - 20,
                                    page_height - height - 20,
                                ),
                            }.get(position, (20, 20))

                        page.insert_image(
                            fitz.Rect(
                                logo_x,
                                logo_y,
                                logo_x + width,
                                logo_y + height,
                            ),
                            stream=logo.content,
                        )

                    keywords = (
                        f"{meta.get('keywords', '')} {MARK}"
                    ).strip()

                    pdf.set_metadata({
                        **meta,
                        'keywords': keywords,
                    })

                    updated_pdf = pdf.tobytes()

                    if updated_pdf:
                        # Avoid triggering this class's write() hook again.
                        super(IrAttachment, record).write({
                            'raw': updated_pdf,
                        })

                        _logger.info(
                            "PDF LOGO DEBUG injection completed: "
                            "attachment=%s name=%s",
                            record.id,
                            record.name,
                        )

                finally:
                    if pdf is not None:
                        pdf.close()

            except Exception:
                _logger.exception(
                    "Failed to inject logo into PDF attachment %s",
                    record.id,
                )
