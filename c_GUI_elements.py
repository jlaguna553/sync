# -*- coding: utf-8 -*-
from f_actions import *


class Elements(object,Frame):

    def __init__(self, root, barra_estado):
        Frame.__init__(self, root, barra_estado)
        #self.iconos = iconos

        self.root = root
        self.barramenu = Menu(self.root)
        self.barra_estado = barra_estado
        self.actions = Actions(self.barra_estado, self)
        self.up = None
        self.up_progress = None
        self.button_up_start = None
        self.button_up_stop = None
        self.down = None
        self.down_progress = None
        self.button_down_start = None
        self.button_down_stop = None

        self.root['menu'] = self.barramenu
        self.e_menu_conexion = Menu(self.barramenu)
        self.e_menu_configuracion = Menu(self.barramenu)
        self.e_menu_ayuda = Menu(self.barramenu)
        self.menu_configuraciones()
        self.menu_connection()
        self.menu_ayuda()
        self.content()

    def content(self):
        self.up = Text(self.root,
                       width=100,
                       height=10)
        self.up.pack()
        self.up.delete('1.0', END)
        self.up.config(state=DISABLED)
        self.up_progress = ttk.Progressbar(orient="horizontal",
                                           length=200,
                                           mode="indeterminate")
        self.up_progress.pack()
        self.button_up_start = Button(text='Sitio => Web',
                                      command=lambda: self.actions.f_start('up', False))
        self.button_up_start.pack()
        self.button_up_stop = Button(text='Stop',
                                     command=lambda: self.actions.f_change_stop('down', True))
        self.button_up_stop.pack()
        self.down = Text(self.root,
                         width=100,
                         height=10)
        self.down.pack()
        self.down.delete('1.0', END)
        self.down.config(state=DISABLED)
        self.down_progress = ttk.Progressbar(orient="horizontal",
                                             length=200,
                                             mode="indeterminate")
        self.down_progress.pack()
        self.button_down_start = Button(text='Web => Sitio',
                                        command=lambda: self.actions.f_start('down', False))
        self.button_down_start.pack()
        self.button_down_stop = Button(text='Stop',
                                       command=lambda: self.actions.f_change_stop('down', True))
        self.button_down_stop.pack()
        self.f_up_messages('Cargar los archivos necesarios subida')
        self.f_down_messages('Cargar los archivos necesarios bajada')
        self.button_up_start.config(state=DISABLED)
        self.button_down_start.config(state=DISABLED)

    def menu_connection(self):
        self.barramenu.add_cascade(menu=self.e_menu_conexion,
                                   label='Conexiones')

        self.e_menu_conexion.add_command(label='Conectar...',
                                         command= lambda: self.actions.f_connection_action(),
                                         underline=1,
                                         compound=LEFT)
        self.e_menu_conexion.add_separator()
        self.e_menu_conexion.add_command(label='Administrador de Conexiones',
                                         command=lambda: self.actions.f_admin_connection_action(),
                                         underline=0,
                                         compound=LEFT)
        self.e_menu_conexion.add_separator()
        self.e_menu_conexion.add_command(label='Crear Conexion',
                                         command = lambda: self.actions.f_create_config_file_action(),
                                         underline = 0,
                                         compound = LEFT)
        self.e_menu_conexion.add_command(label='Ver Conexiones Activas',
                                         command=lambda: self.actions.f_admin_view_files_action(),
                                         underline= 0,
                                         compound= LEFT)
        self.e_menu_conexion.add_command(label ='Añadir una conexion ACTIVA',
                                         command =lambda: self.actions.f_admin_select_file_action(),
                                         underline= 0,
                                         compound = LEFT)

    def menu_configuraciones(self):
        self.barramenu.add_cascade(menu=self.e_menu_configuracion,
                                   label='Archivo')

        self.e_menu_configuracion.add_command(label='Guardar Configuracion...',
                                              command=lambda: self.actions.f_admin_save_configuration_action())

        self.e_menu_configuracion.add_command(label='Cargar Configuracion...',
                                              command=lambda: self.actions.f_admin_load_configuration_action())

        self.e_menu_configuracion.add_separator()

        self.e_menu_configuracion.add_command(label='Salir',
                                              command=self.f_salir)

    def menu_ayuda(self):
        self.barramenu.add_cascade(menu=self.e_menu_ayuda,
                                   label='Acerca de...')
        self.e_menu_ayuda.add_command(label='Acerca de...',
                                      command=None)

    def f_up_messages(self, msg=''):
        self.up.config(state='normal')
        self.up.delete('1.0',END)
        self.up.insert("1.0", msg)
        self.up.config(state=DISABLED)

    def f_down_messages(self, msg=''):
        self.down.config(state='normal')
        self.down.delete('1.0',END)
        self.down.insert("1.0", msg)
        self.down.config(state=DISABLED)

    def f_up_progress(self):
        pass

    def f_salir(self):
        for e in self.actions.pool_connections['up']['origin_connections']:
            if e:
                e.close()
        for e in self.actions.pool_connections['up']['destiny_connections']:
            if e:
                e.close()
        for e in self.actions.pool_connections['down']['origin_connections']:
            if e:
                e.close()
        for e in self.actions.pool_connections['down']['destiny_connections']:
            if e:
                e.close()
        self.root.destroy()


