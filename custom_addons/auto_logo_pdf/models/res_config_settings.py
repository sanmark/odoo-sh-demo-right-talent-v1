from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    logo_position = fields.Selection([
        ('top_left', 'Top Left'),
        ('top_center', 'Top Center'),
        ('top_right', 'Top Right'),
        ('middle_center', 'Middle Center'),
        ('bottom_center', 'Bottom Center'),
        ('bottom_right', 'Bottom Right'),
    ], string="Default Logo Position", default='top_left')

    logo_x = fields.Integer(string="Logo X Position", default=50)
    logo_y = fields.Integer(string="Logo Y Position", default=50)
    logo_width = fields.Integer(string="Logo Width", default=100)
    logo_height = fields.Integer(string="Logo Height", default=50)

    def set_values(self):
        super().set_values()

        config = self.env['ir.config_parameter'].sudo()

        config.set_str('auto_logo_pdf.logo_position', self.logo_position)
        config.set_int('auto_logo_pdf.logo_x', self.logo_x)
        config.set_int('auto_logo_pdf.logo_y', self.logo_y)
        config.set_int('auto_logo_pdf.logo_width', self.logo_width)
        config.set_int('auto_logo_pdf.logo_height', self.logo_height)

    def get_values(self):
        res = super().get_values()

        config = self.env['ir.config_parameter'].sudo()

        res.update(
            logo_position=config.get_str(
                'auto_logo_pdf.logo_position',
                default='top_left',
            ),
            logo_x=config.get_int(
                'auto_logo_pdf.logo_x',
                default=50,
            ),
            logo_y=config.get_int(
                'auto_logo_pdf.logo_y',
                default=50,
            ),
            logo_width=config.get_int(
                'auto_logo_pdf.logo_width',
                default=100,
            ),
            logo_height=config.get_int(
                'auto_logo_pdf.logo_height',
                default=50,
            ),
        )

        return res