from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    logo_x = fields.Integer(string="Logo X Position", default=50)
    logo_y = fields.Integer(string="Logo Y Position", default=50)
    logo_width = fields.Integer(string="Logo Width", default=100)
    logo_height = fields.Integer(string="Logo Height", default=50)

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param('auto_logo_pdf.logo_x', self.logo_x)
        self.env['ir.config_parameter'].sudo().set_param('auto_logo_pdf.logo_y', self.logo_y)
        self.env['ir.config_parameter'].sudo().set_param('auto_logo_pdf.logo_width', self.logo_width)
        self.env['ir.config_parameter'].sudo().set_param('auto_logo_pdf.logo_height', self.logo_height)

    def get_values(self):
        res = super().get_values()
        res.update(
            logo_x=int(self.env['ir.config_parameter'].sudo().get_param('auto_logo_pdf.logo_x', default=50)),
            logo_y=int(self.env['ir.config_parameter'].sudo().get_param('auto_logo_pdf.logo_y', default=50)),
            logo_width=int(self.env['ir.config_parameter'].sudo().get_param('auto_logo_pdf.logo_width', default=100)),
            logo_height=int(self.env['ir.config_parameter'].sudo().get_param('auto_logo_pdf.logo_height', default=50)),
        )
        return res