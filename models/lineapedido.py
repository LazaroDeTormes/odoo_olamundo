from odoo import models, fields, api


class linerapedido(models.Model):
    _name = 'odoo_basico.pedido'
    _description = 'Ejemplo de pedido'

    name = fields.Char(required=True, size=20, string="Línea de pedido")

    descripcion_lp = fields.Text(string="Descripción de la línea de pedido")

    pedido_id = fields.Many2one('odoo_basico.pedido', ondelete="cascade", required=True)

    informacion_ids = fields.Many2many('odoo_basico.informacion',
                                       string="Registro de información",
                                       relation="odoo_basido_lineapedido_informacion",
                                       column1="lineapedido_id", column2="informacion_id")
