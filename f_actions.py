# -*- coding: utf-8 -*-
from _libs import *
import psycopg2.extras
import psycopg2.extensions
from c_threading import *

__configDir__ = 'config'
__logDir__ = 'logs'
__imgDir__ = 'images'
__absolutePath__ = os.path.abspath(os.getcwd())


class Actions(object, Frame):
    def __init__(self, barra_estado, elements):
        Frame.__init__(self, barra_estado)
        self.barra_estado = barra_estado
        self.content = elements
        self.configFiles = {}
        self.pool_connections = {'up':
                                     {'origin_files': {},
                                      'destiny_files': {},
                                      'origin_connections': {},
                                      'destiny_connections': {},
                                      'origin_cursors': {},
                                      'destiny_cursors': {},
                                      'stop' : False
                                      },
                                 'down':
                                     {'origin_files': {},
                                      'destiny_files': {},
                                      'origin_connections': {},
                                      'destiny_connections': {},
                                      'origin_cursors': {},
                                      'destiny_cursors': {},
                                      'stop': False
                                      }
                                 }
        self.ap_config = __absolutePath__+'\\'+__configDir__
        self.ap_log = __absolutePath__+'\\'+__logDir__
        self.file_list = self.f_get_file_list()
        self.connected_flag = False
        self.qry = qry
        #inicializamos los threadings
        self.hilos = {}

    def f_change_stop(self,direction, status):
        self.pool_connections[direction]['stop'] = status


    def f_start(self, direction, status):
        #print direction % self.pool_connections
        self.pool_connections[direction]['stop'] = status
        self.hilo = ThreadStation(self, direction)
        self.hilo.start()

    def f_get_file_list(self):
        return [arch for arch in os.listdir(self.ap_config) if isfile(join(self.ap_config, arch))]

    def f_get_connection_objects(self):
        for k in [key for key in self.configFiles if self.configFiles[key].sitio_externa == 'S']:
            try:
                self.pool_connections['up']['origin_files'][k] = self.configFiles[k]
                self.pool_connections['up']['origin_connections'][k] = self.f_connect_element(self.configFiles[k])
                self.pool_connections['up']['origin_cursors'][k] = self.f_connect_cursor_element(self.configFiles[k],
                                                                                                 self.pool_connections['up']['origin_connections'][k])
                self.pool_connections['down']['destiny_files'][k] = self.configFiles[k]
                self.pool_connections['down']['destiny_connections'][k] = self.f_connect_element(self.configFiles[k])
                self.pool_connections['down']['destiny_cursors'][k] = self.f_connect_cursor_element(self.configFiles[k],
                                                                                                    self.pool_connections['down']['destiny_connections'][k])

                self.content.f_up_messages('Conectado')
                self.content.button_up_start.config(state='normal')
            except Exception as e:
                self.content.f_up_messages('Ocurrio un error de conexión')
                print 'ocurrio un error: %s'%e
        for k in [key for key in self.configFiles if self.configFiles[key].sitio_externa == 'E']:
            try:
                self.pool_connections['down']['origin_files'][k] = self.configFiles[k]
                self.pool_connections['down']['origin_connections'][k] = self.f_connect_element(self.configFiles[k])
                self.pool_connections['down']['origin_cursors'][k] = self.f_connect_cursor_element(self.configFiles[k],
                                                                                                 self.pool_connections[
                                                                                                     'down'][
                                                                                                     'origin_connections'][
                                                                                                     k])
                self.pool_connections['up']['destiny_files'][k] = self.configFiles[k]
                self.pool_connections['up']['destiny_connections'][k] = self.f_connect_element(self.configFiles[k])
                self.pool_connections['up']['destiny_cursors'][k] = self.f_connect_cursor_element(self.configFiles[k],
                                                                                                    self.pool_connections['up']['destiny_connections'][k])
                self.content.f_down_messages('Conectado')
                self.content.button_down_start.config(state='normal')
            except Exception as e:
                self.content.f_down_messages('Ocurrio un error de conexión')
                print 'ocurrio un error %s'%e

    def f_connection_action(self):
        self.barra_estado.update_barra_estado('Conectando...')
        if self.configFiles:
            self.f_get_connection_objects()
            self.barra_estado.update_barra_estado('Conectado')
            #print self.pool_connections
        else:
            self.barra_estado.update_barra_estado('Error de Conexion')

    @staticmethod
    def f_connect_element(file_object):
        if file_object.tipo == 'PG':
            return psycopg2.connect("host='" + file_object.host +
                                    "' dbname='" + file_object.dbname +
                                    "' user='" + file_object.user +
                                    "' password='" + file_object.password + "'")

        elif file_object.tipo == 'FM':
            return pyodbc.connect('DRIVER={FileMaker ODBC};SERVER='+file_object.host +
                                  ';DATABASE='+file_object.dbname +
                                  ';UID='+file_object.user +
                                  ';PWD='+file_object.password)

    @staticmethod
    def f_connect_cursor_element(file_object, connection):
        if file_object.tipo == 'PG':
            psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
            return
        elif file_object.tipo == 'FM':
            return connection.cursor()

    def f_disconnect(self):
        pass

    def f_admin_connection_action(self):
        if not os.path.exists(self.ap_config):
            os.mkdir(self.ap_config)
        w_main_option = eg.buttonbox(msg='Administrador de Conexiones',
                                     title='Powered by InfoExpo',
                                     choices=['Select a Configuration File',
                                             'View Active Files',
                                             'Create a Config File',
                                             'Update Config File',
                                             'Delete Config File',
                                             'Cancel'])

        if w_main_option == 'Select a Configuration File' and self.f_get_file_list():
            self.f_admin_select_file_action()

        elif w_main_option == 'Create a Config File':
            self.f_create_config_file_action()

        elif w_main_option == 'View Active Files':
            self.f_admin_view_files_action()

        elif w_main_option == 'Update Config File':
            self.f_admin_update_file_action()

        elif w_main_option == 'Delete Config File':
            self.f_admin_delete_file_action()

    def f_admin_update_file_action(self, filename=None):
        if not filename:
            w_update_file = eg.choicebox(msg='Selecciona un archivo para actualizar',
                                             title='Powered by InfoExpo',
                                             choices=[str.replace(c, '.txt', '') for c in self.f_get_file_list()])
            if w_update_file == 'Add more choices':
                self.f_create_config_file_action()
            elif not w_update_file:
                self.f_admin_connection_action()
            else:
                LoadConfig(filename=w_update_file, route=self.ap_config, reconfig=True)
        else:
            LoadConfig(filename=filename, route=self.ap_config, reconfig=True)

    def f_admin_select_file_action(self, filename=None):
        if not filename:
            w_select_file = eg.choicebox(msg='Selecciona un archivo de configuración',
                                         title='Powered by InfoExpo',
                                         choices=[str.replace(c, '.txt', '') for c in self.f_get_file_list()])
            if w_select_file == 'Add more choices':
                filename = eg.enterbox(msg='Escribe el nombre del archivo',
                                       title='Crear Archivo',
                                       default='SAS_DEMO',
                                       strip=True,
                                       image=None)
                LoadConfig(filename=filename, route=self.ap_config, reconfig=True)
            elif not w_select_file:
                self.f_admin_connection_action()
            else:
                self.f_admin_select_file_action(w_select_file)
        else:
            #print filename
            self.configFiles[filename] = LoadConfig(filename=filename,
                                                    route=self.ap_config)

    def f_create_config_file_action(self):
        filename = eg.enterbox(msg='Escribe el nombre del archivo',
                               title='Crear Archivo',
                               default='SAS_DEMO',
                               strip=True,
                               image=None)
        LoadConfig(filename=filename, route=self.ap_config, reconfig=True)

    def f_admin_view_files_action(self):
        w_view_file = eg.choicebox(msg='Archivos de Configuracion Activos',
                                     title='Archivos Activos',
                                     choices=[key for key in self.configFiles])
        if w_view_file == 'Add more choices':
            self.f_admin_select_file_action()
        elif not w_view_file:
            pass
        else:
            self.f_admin_view_files_config_action(w_view_file)

    def f_admin_delete_file_action(self):
        w_delete_file = eg.choicebox(msg='Selecciona un archivo para eliminar',
                                     title='Powered by InfoExpo',
                                     choices=[str.replace(c, '.txt', '') for c in self.f_get_file_list()])
        if w_delete_file == 'Add more choices':
            self.f_create_config_file_action()
        elif not w_delete_file:
            self.f_admin_connection_action()
        else:
            os.remove(self.ap_config+'\\'+w_delete_file+'.txt')
            if self.configFiles:
                self.configFiles.pop(w_delete_file)

    def f_admin_save_configuration_action(self):
        if self.configFiles:
            SaveFileConfig(eg.filesavebox(msg='Selecciona la ruta para guardar',
                                          title='Guardar Configuracion'),[key for key in self.configFiles])
        else:
            eg.msgbox(msg='No se ha cargado ningun archivo')

    def f_admin_load_configuration_action(self):
        configFile = LoadFileConfig(eg.fileopenbox(msg='Selecciona un archivo de configuraciones',title='Cargar Archivo de Configuracion'))
        #print configFile.objectsList
        map(self.f_admin_select_file_action,configFile.objectsList)
        #self.configFiles = configFile.objectsList

    def f_admin_view_files_config_action(self,file):
        w_config_file = eg.buttonbox(msg='Selecciona una Accion sobre el Archivo:%s'%file,
                                     title=file,
                                     choices=['Configurar','Quitar de Activos'])
        if w_config_file == 'Configurar':
            self.f_admin_update_file_action(filename=file)
        elif w_config_file == 'Quitar de Activos':
            self.configFiles.pop(file)
        else:
            self.f_admin_view_files_action()

    def data_process(self, direction):
        #base de lectura u origen
        while not self.pool_connections[direction]['stop']:

            getter = [key for key in self.pool_connections[direction]['origin_files']
                      if self.pool_connections[direction]['origin_files'][key].lectura == 'True'][0]
            #print self.pool_connections[direction]['origin_cursors'][getter], qry[getter]['get_data']
            visitors = self.pool_connections[direction]['origin_cursors'][getter].execute(qry[getter]['get_data'])
            if self.pool_connections[direction]['origin_files'][getter].tipo == 'FM':
                visitors = self.get_dictionary_fm(visitors)
            if visitors:
                # creamos en dict

                for visitor in visitors:
                    try:
                        #visitor = self.f_sanitize(visitor)
                        if self.pool_connections[direction]['stop']:
                            break
                        if direction == 'up':
                            self.content.f_up_messages(visitor)
                        elif direction == 'down':
                            self.content.f_down_messages(visitor)
                        #marcamos el visitante en 1 en el origen
                        self.pool_connections[direction]['origin_cursors'][getter].execute(qry[getter]['in_process'] % visitor)
                        self.pool_connections[direction]['origin_connections'][getter].commit()
                        #Empezamos el repaso de las consultas por cada base de destino
                        for key in [key for key in self.pool_connections[direction]['destiny_files']
                                    if self.pool_connections[direction]['destiny_files'][key].escritura == 'True']:
                            #Revisamos si existe el visitante

                            if self.pool_connections[direction]['destiny_files'][key].tipo == 'FM':
                                var = self.get_dictionary_fm(self.pool_connections[direction]['destiny_cursors'][key].execute(qry[key]['exists'] % visitor))
                                varP = self.get_dictionary_fm(self.pool_connections[direction]['destiny_cursors'][key].execute(qry[key]['exist_participation'] % visitor))
                            else:
                                self.pool_connections[direction]['destiny_cursors'][key].execute(qry[key]['exist'] % visitor)
                                var = self.get_dictionary_pg(self.pool_connections[direction]['destiny_cursors'][key])
                                self.pool_connections[direction]['destiny_cursors'][key].execute(qry[key]['exist_participation'])
                                varP = self.get_dictionary_pg(self.pool_connections[direction]['destiny_cursors'][key])
                            if var:
                                visitor['exists'] = int(var[0]['exist'])
                            else:
                                visitor['exists'] = None
                            if varP[0]['existP']:
                                visitor['existsP'] = int(varP[0]['existP'])
                            else:
                                visitor['existsP'] = None
                            print 'entro al ciclo'
                            print visitor['existsP'], visitor['exists']
                            if visitor['existsP']:
                                'paso 3'
                                for k in qry[key]['if_participation']:
                                    '''
                                    print k
                                    print (qry[key]['if_participation'][k] % visitor).replace("'None'",'\'\'').replace('None','0').replace("CAST(\'\' AS TIMESTAMP)",'\'\'')
                                    
                                    self.pool_connections[direction]['destiny_cursors'][key].execute((qry[key]['if_participation'][k] % visitor).replace("'None'",'\'\'').replace('None','0').replace("CAST(\'\' AS TIMESTAMP)",'\'\''))
                                    self.pool_connections[direction]['destiny_connections'][key].commit()
                                    '''
                            elif visitor['exists'] and not visitor['existsP']:
                                print 'paso1'
                                '''
                                print (qry[key]['if_participation']['update_visitor'] % visitor).replace("'None'",'\'\'').replace('None','0').replace("CAST(\'\' AS TIMESTAMP)",'\'\'')
                                print (qry[key]['if_not_exists']['insert_edition_visitor'] % visitor).replace("'None'",'\'\'').replace('None','0').replace("TIMESTAMP ''",'\'\'')
                                self.pool_connections[direction]['destiny_cursors'][key].execute((qry[key]['if_participation']['update_visitor'] % visitor).replace("'None'",'\'\'').replace('None','0').replace("CAST(\'\' AS TIMESTAMP)",'\'\''))
                                self.pool_connections[direction]['destiny_connections'][key].commit()
                                self.pool_connections[direction]['destiny_cursors'][key].execute((qry[key]['if_not_exists']['insert_edition_visitor'] % visitor).replace("'None'",'\'\'').replace('None','0').replace("TIMESTAMP ''",'\'\''))
                                self.pool_connections[direction]['destiny_connections'][key].commit()
                                '''
                            else:
                                for k in qry[key]['if_not_exists']:
                                    print 'paso2'
                                    print k
                                    print (qry[key]['if_not_exists'][k] % visitor)
                                    self.pool_connections[direction]['destiny_cursors'][key].execute((qry[key]['if_not_exists'][k] % visitor).replace("'None'",'\'\'').replace('None','0').replace("TIMESTAMP ''",'\'\''))
                                    self.pool_connections[direction]['destiny_connections'][key].commit()
                        self.pool_connections[direction]['origin_cursors'][getter].execute(qry[getter]['processed'] % visitor)
                        self.pool_connections[direction]['origin_connections'][getter].commit()
                    except:
                        print 'error'
                        self.pool_connections[direction]['origin_cursors'][getter].execute(qry[getter]['in_process'] % visitor)
                        self.pool_connections[direction]['origin_connections'][getter].commit()
            else:
                time.sleep(5)


    def get_dictionary_fm(self, data):
        columns = [column[0] for column in data.description]
        result = []
        for row in data.fetchall():
            result.append(dict(zip(columns, row)))
        return result

    @staticmethod
    def f_sanitize(data):
        for key in data:
            data[key].replace('\'', '')
        return data

    @staticmethod
    def get_dictionary_pg(data):
         return data.fetchall()






    def f_get_icons(self):
        img_carpeta = __absolutePath__+'\\'+__imgDir__
        #print img_carpeta
        iconos = [img_carpeta + "\\pyremoto64x64.gif",
                  img_carpeta + "\\conec16x16.gif",
                  img_carpeta + "\\salir16x16.gif",
                  img_carpeta + "\\star16x16.gif",
                  img_carpeta + "\\conec32x32.gif",
                  img_carpeta + "\\salir32x32.gif"]

        errorIcons = self.f_verificar_iconos(iconos=iconos)

        if not errorIcons:
            return iconos
        else:
            sys.exit()

    def f_verificar_iconos(self,iconos):
        for icono in iconos:
            #print icono
            if not os.path.exists(icono):
                return 1
        return False


