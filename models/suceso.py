from odoo import models, fields, api

class suceso(models.Model):
    _name = 'odoo_basico.suceso'
    _description = 'exemplo para suceso'

    name = fields.Char(required=True, size=20, string="Suceso")
    descripcion = fields.Text(string="A Descripción do Suceso")
    nivel = fields.Selection([('Baixo', 'Baixo'), ('Medio', 'Medio'), ('Alto', 'Alto')], string='Nivel')
    data_hora = fields.Datetime(string="Data e Hora")
