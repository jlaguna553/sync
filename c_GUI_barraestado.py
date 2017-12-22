from f_actions import *


class barra_estado (object, Frame):

    def __init__(self,master):
        Frame.__init__(self, master)
        #self.barra_estado = IntVar()
        #self.barra_estado.set(1)
        self.informacion_system = platform.system()
        self.informacion_node = platform.node()
        self.informacion_machine = platform.machine()
        self.mensaje = ' '+ self.informacion_system + ' ' + self.informacion_node + ' ' + self.informacion_machine
        self.barra_estado = Label(self.master, text=self.mensaje, bd=1, relief=SUNKEN, anchor=W)
        self.barra_estado.pack(side=BOTTOM, fill=X)

    def update_barra_estado(self,msj):
        self.barra_estado.config(text=self.mensaje + ' - ' + msj)