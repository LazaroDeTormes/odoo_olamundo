# -*- coding: utf-8 -*-

from odoo import models, fields, api


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'exemplo'

    name = fields.Char(string="Título:")
    descripcion = fields.Char(string="Descripción:")
    peso = fields.Float(string="Peso:")
    sexo_traducido = fields.Selection([('Hombre','Home'),('Mujer','Muller'),('Sin especificar','Sen especificar')], string="Sexo:")
    autorizado = fields.Boolean(string="¿Autorizado?:", default=True)
    alto_en_cms = fields.Integer(string="Alto en centímetros:")
    ancho_en_cms = fields.Integer(string="Ancho en centímetros:")
    largo_en_cms = fields.Integer(string="Largo en centímetros:")