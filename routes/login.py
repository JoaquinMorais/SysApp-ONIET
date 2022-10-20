from crypt import methods
from flask import Blueprint,render_template,redirect,url_for,request,session,g,abort,flash,jsonify
from models.databases import Usuarios
from utils.db import db

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
        pw = request.form['password']
        usuario = Usuarios.query.filter_by(username = nm).all()
        
        if len(usuario)!=0 and usuario[0].password == pw:
            global user
        
            user = usuario[0]
            return redirect(url_for('Login.profile'))



    return render_template("login/login.html")




@Login.route("/profile")
def profile():
    global user
    g.usuario = user
    return render_template("login/profile.html")














