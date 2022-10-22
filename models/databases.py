from math import trunc

from sqlalchemy import null
from utils.db import db
import crypt
from datetime import date
from dateutil import relativedelta as rd
import random
"""
class ExampleDatabase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    describe = db.Column(db.String(300))


    def __init__(self,name,describe):
        self.name = name
        self.describe = describe
    
    def __repr__(self):
        return f'<id: {self.id}, name: "{self.name}", describe: "{self.describe}">'
"""


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    idUsuario = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    plataTotal = db.Column(db.Integer)
    meta = db.Column(db.Integer)
    direccionFoto = db.Column(db.String(100))

    registros = db.relationship('Registros')
    sueldos = db.relationship('Sueldos')

    def __init__(self,username,password):
        self.username = username
        self.password = crypt.crypt(password, 'salt')
        self.plataTotal = 0
        self.meta = 0
        self.direccionFoto = f'src/logos/{random.randint(1,11)}.png'
    
    def __repr__(self):
        return f'<id: {self.idUsuario}, name: "{self.username}", describe: "{self.password}">'

    def registro_plata(self):
        return [{'x':x.fecha,'y':x.plataTotal} for x in self.registros]

    def registro_ingreso(self):
        return [{'x':x.fecha,'y':x.monto} for x in self.registros if x.tipo == '+' or x.tipo == '=']
    
    def registro_gasto(self):
        return [{'x':x.fecha,'y':x.monto} for x in self.registros if x.tipo == '-']

    def registro_caractGasto(self):
        return [
            {'nombre':'OCIO','porcentaje':self.porcentaje_ocio()},
            {'nombre':'IMPUESTOS','porcentaje':self.porcentaje_impuestos()},
            {'nombre':'SALUD','porcentaje':self.porcentaje_salud()},
            {'nombre':'SERVICIOS','porcentaje':self.porcentaje_servicios()},
            {'nombre':'GASTRONOMIA','porcentaje':self.porcentaje_gastronomia()},
            {'nombre':'COMPRAS','porcentaje':self.porcentaje_compras()},
            {'nombre':'OTROS','porcentaje':self.porcentaje_otros()},
        ]

    def modificar_registro(self,monto,descripcion,tipo):
        if (len(self.registros) >= 2):
            self.plataTotal = self.registros[-2].plataTotal
            self.registros[-1].modificar(monto,descripcion,tipo)
        else:
            self.plataTotal = 0
            self.registros[0].modificar(monto,descripcion,'=')
    
    def ingresos_totales(self):
        return sum([x.monto for x in self.registros if x.tipo == '+' or x.tipo == '='])
    
    def gastos_totales(self):
        gastos = sum([x.monto for x in self.registros if x.tipo == '-'])
        if gastos == 0:
            return 1
        return gastos

    
    
    def porcentaje_ocio(self):
        valor = sum([x.monto for x in self.registros if x.tipo == '-' and x.caracteristica == 'ocio'])
        return trunc(((valor*100)/self.gastos_totales())*100)/100

    def porcentaje_impuestos(self):
        valor =  sum([x.monto for x in self.registros if x.tipo == '-' and x.caracteristica == 'impuestos'])
        return trunc(((valor*100)/self.gastos_totales())*100)/100
    
    def porcentaje_salud(self):
        valor =  sum([x.monto for x in self.registros if x.tipo == '-' and x.caracteristica == 'salud'])
        return trunc(((valor*100)/self.gastos_totales())*100)/100
    
    def porcentaje_servicios(self):
        valor =  sum([x.monto for x in self.registros if x.tipo == '-' and x.caracteristica == 'servicios'])
        return trunc(((valor*100)/self.gastos_totales())*100)/100
    
    def porcentaje_gastronomia(self):
        valor =  sum([x.monto for x in self.registros if x.tipo == '-' and x.caracteristica == 'gastronomia'])
        return trunc(((valor*100)/self.gastos_totales())*100)/100
    
    def porcentaje_compras(self):
        valor =  sum([x.monto for x in self.registros if x.tipo == '-' and x.caracteristica == 'compras'])
        return trunc(((valor*100)/self.gastos_totales())*100)/100
    
    def porcentaje_otros(self):
        valor =  sum([x.monto for x in self.registros if x.tipo == '-' and x.caracteristica not in ['ocio','impuestos','salud','servicios','gastronomia','compras']])
        return trunc(((valor*100)/self.gastos_totales())*100)/100
    
    def len_registros(self):
        return len(self.registros)
    
    def ultimos_registros(self):
        if self.len_registros() == 0:
            return None
        elif self.len_registros() >=10:
            lista = self.registros[-10:]
        else:
            lista = self.registros
        lista_reverse = []
        largo = len(lista)
        for i in range(largo):
            lista_reverse.append(lista[largo-(1+i)])
        return lista_reverse





class Registros(db.Model):
    __tablename__ = 'registros'
    idRegistro = db.Column(db.Integer, primary_key = True)
    monto = db.Column(db.Integer)
    descripcion = db.Column(db.String(100))
    tipo = db.Column(db.String(1))
    fecha = db.Column(db.Date)
    plataTotal = db.Column(db.Integer)
    caracteristica = db.Column(db.String(25))

    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'))
    usuario = db.relationship('Usuarios')

    def __init__(self,monto,descripcion,tipo,fecha,idUsuario,caracteristica):
        self.monto = monto
        self.descripcion = descripcion
        self.tipo = tipo
        self.fecha = fecha
        self.idUsuario = idUsuario 
        self.caracteristica = ' '
        if caracteristica != None:
            self.caracteristica = caracteristica.lower()
        
        self.plataTotal = 0
        
    
    def añadir_plata(self):        
        if self.tipo == '=':
            self.usuario.plataTotal = self.monto
            self.plataTotal = self.monto     
        elif self.tipo == '+':
            self.usuario.plataTotal += self.monto
            self.plataTotal = self.usuario.plataTotal
        else:
            self.usuario.plataTotal -= self.monto
            self.plataTotal = self.usuario.plataTotal
    
    def modificar(self,monto,descripcion,tipo):
        self.monto = monto
        self.descripcion = descripcion
        self.tipo = tipo
        self.añadir_plata()
        
    
    def __repr__(self):
        return f'<Registros: {self.idRegistro}>'



class Sueldos(db.Model):
    __tablename__ = 'sueldos'
    idSueldo = db.Column(db.Integer, primary_key = True)
    monto = db.Column(db.Integer)
    descripcion = db.Column(db.String(100))
    fecha = db.Column(db.Date)
    
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'))
    usuario = db.relationship('Usuarios')

    def __init__(self,monto,descripcion,fecha,idUsuario):
        self.monto = monto
        self.descripcion = descripcion
        self.fecha = fecha
        self.idUsuario = idUsuario 
          
    def __repr__(self):
        return f'<Registros: {self.idSueldo}>'

    def next_month(self):
        if self.fecha <= date.today():
            self.fecha += rd.relativedelta(months = 1)
            return True
        return False
