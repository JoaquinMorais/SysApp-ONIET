from utils.db import db
import crypt
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

    registros = db.relationship('Registros')

    def __init__(self,username,password):
        self.username = username
        self.password = crypt.crypt(password, 'salt')
        self.plataTotal = 0
    
    def __repr__(self):
        return f'<id: {self.idUsuario}, name: "{self.username}", describe: "{self.password}">'

    def plata_total(self):
        return [{'x':x.fecha,'y':x.plataTotal} for x in self.registros]

    def modificar_registro(self,monto,descripcion,tipo):
        if (len(self.registros) >= 2):
            self.plataTotal = self.registros[-2].plataTotal
            self.registros[-1].modificar(monto,descripcion,tipo)
        else:
            self.plataTotal = 0
            self.registros[0].modificar(monto,descripcion,'=')
        

class Registros(db.Model):
    __tablename__ = 'registros'
    idRegistro = db.Column(db.Integer, primary_key = True)
    monto = db.Column(db.Integer)
    descripcion = db.Column(db.String(100))
    tipo = db.Column(db.String(1))
    fecha = db.Column(db.Date)
    plataTotal = db.Column(db.Integer)
    
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'))
    usuario = db.relationship('Usuarios')

    def __init__(self,monto,descripcion,tipo,fecha,idUsuario):
        self.monto = monto
        self.descripcion = descripcion
        self.tipo = tipo
        self.fecha = fecha
        self.idUsuario = idUsuario 
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
