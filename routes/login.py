from flask import Blueprint,render_template,redirect,url_for,request,session,g,abort,flash,jsonify
from models.databases import Usuarios,Registros,Sueldos
from utils.db import db
from datetime import date
from dateutil import relativedelta
import crypt
from .graficos import CreatePlotIE,CreatePlotPT,CreateBarPlot,CreatePlot

Login = Blueprint("Login",__name__)




    

@Login.before_request
def before_request():
    if 'user_id' in session:
        try:
            usuario = Usuarios.query.filter_by(idUsuario = session['user_id']).all()[0]
            g.user = usuario
        except:
            pass
    else:
        g.user = None



@Login.route("/singin",methods=['GET','POST'])
def singin():
    if request.method == 'POST':
        session.pop('user_id',None)
        username = request.form['username']
        password = request.form['password']

        database = Usuarios.query.all()
        print(f'Values {username}, {password}')
        user = ([x for x in database if x.username == username]+[False])[0]
        
        if user != False:
            flash(f'Este nombre de usuario ya ha sido seleccionado, intentelo nuevamente')
            return redirect(url_for('Login.singin'))
        else:
            newInstance = Usuarios(username,password)
            db.session.add(newInstance)
            db.session.commit()
            session['user_id'] = newInstance.idUsuario
        return redirect(url_for('Login.profile'))
        

    flash('')
    return render_template("login/singin.html")




@Login.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id',None)
        nm = request.form['username']
        pw = crypt.crypt(request.form['password'], 'salt')
        usuario = Usuarios.query.filter_by(username = nm).all()
        
        if len(usuario)!=0 and usuario[0].password == pw:
        
            user = usuario[0]
            session['user_id'] = user.idUsuario
            return redirect(url_for('Login.profile'))



    return render_template("login/login.html")




@Login.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for('Login.login'))
    
    

    for sueldo in g.user.sueldos:
        fecha = sueldo.fecha
        while sueldo.next_month():
            newInstance = Registros(int(sueldo.monto),sueldo.descripcion,'+',fecha,g.user.idUsuario,None)
            db.session.add(newInstance)
            db.session.commit()
            newInstance.añadir_plata()
            db.session.commit()


    return render_template("login/profile.html")

@Login.route("/registro",methods=['GET','POST'])
def registro():

    if not g.user:
        return redirect(url_for('Login.login'))
    else:
        if request.method == 'POST':
            try:
                mt = request.form['monto']
                tp = request.form['tipo']
                desc = request.form['descripcion']
                try:
                    carc = request.form['caracteristica']
                except:
                    carc = None
            except:
                return redirect(url_for('Login.registro'))
            newInstance = Registros(int(mt),desc,tp,date.today(),g.user.idUsuario,carc)
            db.session.add(newInstance)
            db.session.commit()
            newInstance.añadir_plata()
            db.session.commit()
            return redirect(url_for('Login.profile'))
        else:
            return render_template("login/registro.html")
    
@Login.route("/sueldo",methods=['GET','POST'])
def sueldo():
    if not g.user:
        return redirect(url_for('Login.login'))
    else:
        if request.method == 'POST':
            try:
                mt = request.form['sueldo']
                fc = request.form['fecha']
                desc = request.form['descripcion']
            except:
                return redirect(url_for('Login.sueldo'))
            print(fc)
            if date(int(fc[0:4]),int(fc[5:7]),int(fc[-2:])) > date.today():
                newInstance = Sueldos(int(mt),desc,fc,g.user.idUsuario)
                db.session.add(newInstance)
                db.session.commit()
            
                return redirect(url_for('Login.profile'))
            return redirect(url_for('Login.sueldo'))
        else:
            return render_template("login/sueldo.html")

@Login.route("/meta",methods=['GET','POST'])
def meta():

    if not g.user:
        return redirect(url_for('Login.login'))
    else:
        if request.method == 'POST':
            try: 
                met = request.form['meta']
            except:
                return redirect(url_for('Login.meta'))
            g.user.meta = int(met)
            db.session.commit()
            return redirect(url_for('Login.profile'))
        else:
            return render_template("login/meta.html")


@Login.route("/añadir")
def añadir():
    newUser = Usuarios('Admin','Admin')
    newInstance1 = Registros(500,'auto','=','2022-03-10',1,None)
    newInstance2 = Registros(1000,'chupetin','-','2022-05-21',1,'gastronomia')
    newInstance3 = Registros(1500,'alfajor','+','2022-08-03',1,None)
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



