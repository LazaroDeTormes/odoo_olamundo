# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import ValidationError


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'exemplo'
    _sql_constraints = [('nomeUnico', 'unique(name)', 'Non se pode repetir o nome')]
    _order = "descripcion desc"

    name = fields.Char(string="Título:")
    descripcion = fields.Char(string="Descripción:")
    peso = fields.Float(digits=(6, 2), string="Peso en Kg.s")
    sexo_traducido = fields.Selection([('Hombre', 'Home'), ('Mujer', 'Muller'), ('Sin especificar', 'Sen especificar')],
                                      string="Sexo:")
    literal = fields.Char(store=False)
    autorizado = fields.Boolean(string="¿Autorizado?:", default=True)
    alto_en_cms = fields.Float(string="Alto en centímetros:")
    ancho_en_cms = fields.Float(string="Ancho en centímetros:")
    largo_en_cms = fields.Float(string="Largo en centímetros:")
    volume = fields.Float(compute="_volume", store=True, string="Volumen: ")
    densidade = fields.Float(compute="_densidade", store=True, string="Densidad")

    foto = fields.Binary(string='Foto')
    adxunto_nome = fields.Char(string="Nome Adxunto")
    adxunto = fields.Binary(string="Arquivo adxunto")

    # moneda_id = fields.Many2one('res.currency', domain="[('position','=','after')]")
    #
    # gasto_en_euros = fields.Monetary("Gasto en Euros", 'moneda_euro_id')

    @api.depends('alto_en_cms', 'ancho_en_cms', 'largo_en_cms')
    def _volume(self):
        try:
            for rexistro in self:
                rexistro.volume = (float(rexistro.alto_en_cms) * float(rexistro.ancho_en_cms) * float(
                    rexistro.largo_en_cms)) / 1000000
        except Exception as error:
            print(error)

    @api.depends('peso', 'volume')
    def _densidade(self):
        try:
            for rexistro in self:
                rexistro.densidade = (float(rexistro.peso) / float(rexistro.volume)) / 1000
        except Exception as error:
            print(error)

    @api.onchange('alto_en_cms')
    def _avisoAlto(self):
        for rexistro in self:
            if rexistro.alto_en_cms > 7:
                rexistro.literal = 'O alto ten un valor posiblemente excesivo %s é maior que 7' % rexistro.alto_en_cms
            else:
                rexistro.literal = ""

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):  # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.peso < 1 or rexistro.peso > 10:
                raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)
