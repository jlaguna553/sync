# -*- coding: utf-8 -*-

#Declaramos unas variables globales
__author__ = 'Javier Laguna (infoexpo)'
__title__ = 'PySync'
__date__ = ''
__version__ = '2.0'
__licence__ = ''
from _libs import *
from c_GUI_elements import *
from c_GUI_barraestado import *

class screenBase(object):
    def __init__(self):

        self.raiz = Tk()
        #self.iconos = f_get_icons()
        self.raiz.title("PySy"+__version__)
        #self.icono1 = PhotoImage(file = self.iconos[0])
        #self.raiz.iconphoto(self.raiz,self.icono1)
        self.raiz.option_add("*Font","Helvetica 12")
        self.raiz.option_add("*tearOff",False)
        self.raiz.minsize(900,400)
        self.barra_estado = barra_estado(self.raiz)
        self.elements = Elements(self.raiz, self.barra_estado)
        self.barra_estado.update_barra_estado('Iniciando entorno...')
        self.barra_estado.update_barra_estado('No Conectado')
        self.raiz.mainloop()


