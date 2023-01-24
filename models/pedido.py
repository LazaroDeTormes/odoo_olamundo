from odoo import models, fields, api


class pedido(models.Model):
    _name = 'odoo_basico.pedido'
    _description = 'Ejemplo de pedido'

    name = fields.Char(required=True, size=20, string='Pedido')
    fecha_hora = fields.Datetime(string="Fecha y hora")
    lineapedido_id = fields.One2many("odoo_basico.lineapedido", 'pedido_id')

    def actualizadorSexo(self):
        informacion_ids = self.env['odoo_basico.informacion'].search([('autorizado', '=', False)])
        for rexistro in informacion_ids:
            self.env['odoo_basico.informacion']._cambia_campo_sexo(rexistro)

    def creaRexistroInformacion(self):
        creado_id = self.env['odoo_basico.informacion'].create({'name': 'Creado dende pedido'})
        creado_id.descripcion = "Creado dende o modelo pedido"
        creado_id.autorizado = False

    def actualizaRexistroInformacion(self):
        informacion_id = self.env['odoo_basico.informacion'].search([('name', '=', 'Creado dende pedido')])
        if informacion_id:
            informacion_id.name = "Actualizado ..."
            informacion_id.descripcion = "Actualizado dende o modelo pedido"
            informacion_id.sexo_traducido = "Mujer"
