# -*- coding: utf-8 -*-
import os
import easygui as eg
from f_AESCipher import *

class AppConfig(eg.EgStore):
    def __init__(self, filename):
        self.host = ""
        self.dbname = ""
        self.user = ""
        self.password = ""
        self.tipo = ""
        self.lectura = ""
        self.escritura = ""
        self.sitio_externa = ""
        self.filename = filename
        self.relative_name = ""
        self.objectsList = []



def LoadFileConfig(route):
    MiConfig = AppConfig(route)
    MiConfig.restore()
    #print MiConfig
    return MiConfig

def SaveFileConfig(route,objectsList):
    MiConfig =AppConfig(route)
    MiConfig.restore()
    MiConfig.objectsList = objectsList
    MiConfig.store()

def LoadConfig(filename,route,reconfig=False):
    car = route
    ArchivoConfig = os.path.join(car,"",filename+'.txt')
    MiConfig = AppConfig(ArchivoConfig)
    MiConfig.restore()
    if MiConfig.host == '' or MiConfig.dbname == '' or MiConfig.user == '' or MiConfig.password == '' or reconfig:
        host = decrypt(MiConfig.host)
        dbname = decrypt(MiConfig.dbname)
        user = decrypt(MiConfig.user)
        password = decrypt(MiConfig.password)
        tipo = decrypt(MiConfig.tipo)
        lectura = decrypt(MiConfig.lectura)
        escritura = decrypt(MiConfig.escritura)
        sitio_externa = decrypt(MiConfig.sitio_externa)
        campos = ['Host', 'Nombre DB', 'Usuario','Tipo de Base(PG/FM)','Lectura(True/False)','Escritura(True/False)','Sitio/Externa(S/E)','Password']
        data = [host, dbname, user, tipo, lectura, escritura, sitio_externa, password]
        msg = eg.multpasswordbox(msg='Set data base information',
                                title='Config File Data',
                                fields=campos, values=data)

        MiConfig.host = encrypt(msg[0])
        MiConfig.dbname = encrypt(msg[1])
        MiConfig.user = encrypt(msg[2])
        MiConfig.lectura = encrypt(msg[4])
        MiConfig.escritura = encrypt(msg[5])
        MiConfig.sitio_externa = encrypt(msg[6])
        MiConfig.password = encrypt(msg[7])
        MiConfig.tipo = encrypt(msg[3])
        MiConfig.relative_name = encrypt(filename)
        MiConfig.store()

    MiConfig.restore()
    MiConfig.lectura = decrypt(MiConfig.lectura)
    MiConfig.escritura = decrypt(MiConfig.escritura)
    MiConfig.password = decrypt(MiConfig.password)
    MiConfig.host = decrypt(MiConfig.host)
    MiConfig.dbname = decrypt(MiConfig.dbname)
    MiConfig.user = decrypt(MiConfig.user)
    MiConfig.tipo = decrypt(MiConfig.tipo)
    MiConfig.sitio_externa = decrypt(MiConfig.sitio_externa)
    MiConfig.relative_name = decrypt(MiConfig.relative_name)

    return MiConfig

