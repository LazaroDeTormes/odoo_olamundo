# -*- coding: utf-8 -*-
import locale
import os

from odoo import models, fields, api

from odoo.exceptions import ValidationError, RedirectWarning
from odoo.tools.safe_eval import pytz

from . import misUtilidades


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

    moneda_euro_id = fields.Many2one('res.currency',
                                default=lambda self: self.env['res.currency'].search([('name', '=', 'EUR')], limit=1))

    moneda_id = fields.Many2one('res.currency', domain="[('position','=','after')]")

    gasto_en_euros = fields.Monetary("Gasto en Euros", 'moneda_euro_id')

    moneda_en_texto = fields.Char(relaed="moneda_id.currency_unit_label", string="Moneda en formato de texto", store=True)

    creador_de_moneda = fields.Char(related="moneda_id.create_uid.login",
                                   string="Usuario creador de la moneda", store=True)

    fecha = fields.Date(string="Fecha", default=lambda self: fields.Date.today())
    fecha_hora = fields.Datetime(string="Fecha y Hora", default=lambda self: fields.Datetime.now())
    hora_utc = fields.Char(compute="_hora_utc", string="Hora UTC", size=15, store=True)
    hora_actual = fields.Char(compute="_hora_actual", string="Hora Actual", size=15, store=True)
    zona_horaria_usuario = fields.Char(compute="_hora_zona_horaria_usuario", string="Zona Horaria del Usuario", size=15,
                                        store=True)
    mes_castellano = fields.Char(compute="_mes_castellano", size=15, string="Mes castellano", store=True)
    mes_galego = fields.Char(compute="_mes_galego", size=15, string="Mes galego", store=True)

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

    def _cambia_campo_sexo(self, rexistro):
        rexistro.sexo_traducido = "Hombre"

    def ver_contexto(self):
        for registro in self:
            action = self.env.ref('odoo_basico.informacion_list_action')

            contexto = registro.env.context
            msg = 'Contexto: %s Ruta: %s Contenido %s' % (contexto, os.getcwd(), os.listdir(os.getcwd()))
            raise RedirectWarning(msg, action.id, ('Aceptar'))
        return True

    @api.depends('fecha_hora')
    def _hora_utc(self):
        for registro in self:
            registro.hora_utc = registro.fecha_hora.strftime("%H:%M:%S")

    def actualiza_hora_actual_UTC(self):
        for registro in self:
            registro.hora_actual = fields.Datetime.now().strftime("%H:%M:%S")


    @api.depends('fecha_hora')
    def _hora_actual(self):
        for registro in self:
            registro.actualiza_hora_actual_UTC()

    def convierte_fecha_hora_de_utc_a_zona_horaria_de_usuario(self, fecha_hora_utc_object):
        usuario_zona_horaria = pytz.timezone(
            self.env.user.tz or 'UTC')
        return pytz.UTC.localize(fecha_hora_utc_object).astimezone(usuario_zona_horaria)

    def actualiza_hora_zona_horaria_usuario(self, obxeto_rexistro):
        obxeto_rexistro.zona_horaria_usuario = self.convierte_fecha_hora_de_utc_a_zona_horaria_de_usuario(
            obxeto_rexistro.fecha_hora).strftime("%H:%M:%S")

    def actualiza_hora_zona_horaria_usuario_dende_boton_e_apidepends(self):
        self.actualiza_hora_zona_horaria_usuario(self)

    @api.depends('fecha_hora')
    def _hora_zona_horaria_usuario(self):
        for registro in self:
            registro.actualiza_hora_zona_horaria_usuario_dende_boton_e_apidepends()

    # Podemos  configurar locales a nivel de sistema con dpkg-reconfigure locales poñendo un por defecto.
    # apt-get install locales
    # dpkg-reconfigure locales (podemos configurar varios)
    # locale (ver o locale por defecto)
    # locale -a (ver os dispoñibles)

    @api.depends('fecha')
    def _mes_castellano(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, misUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))
        for registro in self:
            registro.mes_castellano = registro.fecha.strftime("%B")  # strftime https://strftime.org/

    @api.depends('fecha')
    def _mes_galego(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, misUtilidades.cadeaTextoSegunPlataforma('Galician_Spain.1252', 'gl_ES.utf8'))
        for registro in self:
            registro.mes_galego = registro.fecha.strftime("%B")
        locale.setlocale(locale.LC_TIME, misUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))