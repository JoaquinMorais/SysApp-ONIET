from utils.db import db

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

    registros = db.relationship('Registros')

    def __init__(self,username,password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'<id: {self.idUsuario}, name: "{self.username}", describe: "{self.password}">'

class Registros(db.Model):
    __tablename__ = 'registros'
    idRegistro = db.Column(db.Integer, primary_key = True)
    monto = db.Column(db.Integer)
    descripcion = db.Column(db.String(100))
    tipo = db.Column(db.String(1))
    fecha = db.Column(db.Date)
    plataTotal = db.Column(db.Integer)
    
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'))
    


    def __init__(self,monto,descripcion,tipo,fecha,plataTotal,idUsuario):
        self.monto = monto
        self.descripcion = descripcion
        self.tipo = tipo
        self.fecha = fecha
        self.plataTotal = plataTotal
        self.idUsuario = idUsuario
    
    def __repr__(self):
        return f'<Registros: {self.idRegistro}>'
