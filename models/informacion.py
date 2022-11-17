# -*- coding: utf-8 -*-

from odoo import models, fields, api


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'exemplo'

    name = fields.Char(string="Título:")
    descripcion = fields.Char(string="Descripción:")
    peso = fields.Float(string="Peso:")
    sexo_traducido = fields.Selection([('Hombre', 'Home'), ('Mujer', 'Muller'), ('Sin especificar', 'Sen especificar')],
                                      string="Sexo:")
    literal = fields.Char(store=False)
    autorizado = fields.Boolean(string="¿Autorizado?:", default=True)
    alto_en_cms = fields.Integer(string="Alto en centímetros:")
    ancho_en_cms = fields.Integer(string="Ancho en centímetros:")
    largo_en_cms = fields.Integer(string="Largo en centímetros:")
    volume = fields.Float(compute="_volume", store=True, string="Volumen: ")
    densidade = fields.Float(compute="_densidade", store=True, string="Densidad")


    @api.depends('alto_en_cms', 'ancho_en_cms', 'largo_en_cms')
    def _volume(self):
        try:
            for rexistro in self:
                rexistro.volume = (float(rexistro.alto_en_cms) * float(rexistro.ancho_en_cms) * float(rexistro.largo_en_cms))/1000000
        except Exception as error:
            print(error)

    @api.depends('peso', 'volume')
    def _densidade(self):
        try:
            for rexistro in self:
                rexistro.densidade = (float(rexistro.peso) / float(rexistro.volume))/1000
        except Exception as error:
            print(error)

    @api.onchange('alto_en_cms')
    def _avisoAlto(self):
        for rexistro in self:
            if rexistro.alto_en_cms > 7:
                 rexistro.literal = 'O alto ten un valor posiblemente excesivo %s é maior que 7' % rexistro.alto_en_cms
            else:
                 rexistro.literal = ""