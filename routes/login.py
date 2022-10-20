from flask import Blueprint,render_template,redirect,url_for,request,session,g,abort,flash,jsonify
from models.databases import Usuarios,Registros
from utils.db import db
from datetime import date
import crypt

Login = Blueprint("Login",__name__)




    

user = None


@Login.route("/singin",methods=['GET','POST'])
def singin():
    if request.method == 'POST':
        global user
        username = request.form['username']
        password = request.form['password']

        database = Usuarios.query.all()
        print(f'Values {username}, {password}')
        user = ([x for x in database if x.username == username]+[False])[0]
        print
        
        if user != False:
            flash(f'Este nombre de usuario ya ha sido seleccionado, intentelo nuevamente')
            return redirect(url_for('Login.singin'))
        else:
            newInstance = Usuarios(username,password)
            db.session.add(newInstance)
            db.session.commit()
            user = newInstance

        return redirect(url_for('Login.profile'))
        

    flash('')
    return render_template("login/singin.html")


@Login.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        nm = request.form['username']
        pw = crypt.crypt(request.form['password'], 'salt')
        usuario = Usuarios.query.filter_by(username = nm).all()
        
        if len(usuario)!=0 and usuario[0].password == pw:
            global user
        
            user = usuario[0]
            return redirect(url_for('Login.profile'))



    return render_template("login/login.html")




@Login.route("/profile")
def profile():
    global user
    if user:
        g.usuario = user
        return render_template("login/profile.html")
    return redirect(url_for('Login.login'))


@Login.route("/registro")
def returnRegistro():
    return render_template("login/registro.html")

@Login.route("/sueldo")
def returnSueldo():
    return render_template("login/sueldo.html")



@Login.route("/añadir")
def añadir():
    newUser = Usuarios('Admin','Admin')
    newInstance1 = Registros(500,'auto','=','2022-03-10',1)
    newInstance2 = Registros(1000,'chupetin','-','2022-05-21',1)
    newInstance3 = Registros(1500,'alfajor','+','2022-08-03',1)
    db.session.add(newUser)
    db.session.add(newInstance1)
    db.session.add(newInstance2)
    db.session.add(newInstance3)
    db.session.commit()
    newInstance1.añadir_plata()
    newInstance2.añadir_plata()
    newInstance3.añadir_plata()
    db.session.commit()
    return 'Añadido!!'

@Login.route("/mostrar")
def mostrar():
    user = Usuarios.query.all()[0]
    user.modificar_registro(5,'sueldo','+')
    db.session.commit()

    return 'nashe'












