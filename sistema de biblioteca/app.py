from email import header

from time import strftime
from flask import Flask, request, session, redirect, url_for, render_template,flash, Response
from flaskext.mysql import MySQL #importa archivos de mysql
from flask import send_from_directory
from datetime import datetime
from notifypy import Notify
import pymysql 
import re 
import os
from datetime import date
from datetime import datetime
from fpdf import FPDF

app = Flask(__name__)
 
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'cairocoders-ednalan'
app.secret_key="Develoteca"
 
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testingdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

 
# http://localhost:5000/pythonlogin/ - this will be the login page
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accountss WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
   
    # If account exists in accountss table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Nombre de usuario/contraseña incorrectos'
    
    return render_template('index.html', msg=msg)
 

# http://localhost:5000/register - this will be the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # conecta
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
   
  #Check if account exists using MySQL
        cursor.execute('SELECT * FROM accountss WHERE username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'La cuenta ya existe!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Dirección de correo electrónico no válida!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'El nombre de usuario debe contener solo caracteres y números!'
        elif not username or not password or not email:
            msg = 'Por favor rellena el formulario!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accountss table
            cursor.execute('INSERT INTO accountss VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email)) 
            conn.commit() #almacena
   
            msg = 'Se ha registrado exitosamente!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Por favor rellena el formulario!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
  


# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
   
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
  
# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
 
# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile(): 
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accountss WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
  


@app.route('/crud')
def crud():
    sql = "SELECT * FROM  `accountss`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)  
    accountss=cursor.fetchall() #selecciona registros
    print(accountss) #muestra registros
    conn.commit()
    return render_template('crud.html', accountss=accountss )



@app.route('/destroy/<int:id>')
def destroy(id):
    conn= mysql.connect()
    cursor=conn.cursor()    
    cursor.execute("DELETE FROM accountss WHERE id=%s",(id))
    conn.commit()
    return redirect('/')


@app.route('/edit/<int:id>')
def edit(id):
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM accountss WHERE id=%s",(id))   
    accountss=cursor.fetchall() #selecciona registros
    conn.commit() 
    return render_template('edit.html',accountss=accountss)
 

@app.route('/update', methods=['POST'])
def update():

    fullname=request.form['txtNombre']
    username=request.form['txtUsername']
    password=request.form['txtContraseña']
    email=request.form['txtCorreo']    
    id=request.form['txtID']
    sql ="UPDATE accountss SET fullname=%s, username=%s, password=%s, email=%s WHERE  id=%s ;"

    datos=(fullname,username,password,email,id)  
    conn= mysql.connect()
    cursor=conn.cursor()

    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/store', methods=['POST'])
def storage():
    fullname=request.form['txtNombre']
    username=request.form['txtUsername']
    password=request.form['txtContraseña']
    email=request.form['txtCorreo']
  
    sql = "INSERT INTO `accountss` (`id`, `fullname`, `username`, `password`,`email`) VALUES (NULL, %s, %s, %s, %s);"
    
    datos=(fullname,username,password,email)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')



# http://localhost:5000/register - this will be the registration page

@app.route('/libros', methods=['GET', 'POST'])
def libros():
    # conecta
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'libro' in request.form and 'fecha' in request.form:
        # Create variables for easy acces

        libro = request.form['libro']
        fecha = request.form['fecha']
        
  #Check if account exists using MySQL
        cursor.execute('SELECT * FROM lib WHERE libro = %s', (libro))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if not libro:
            msg = 'Por favor rellena el formulario!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accountss table
            cursor.execute('INSERT INTO lib VALUES (NULL, %s, %s)', (libro, fecha)) 
            conn.commit() #almacena
   
            msg = 'Se ha registrado exitosamente!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Por favor rellena el formulario!'
    # Show registration form with message (if any)
    return render_template('libros.html', msg=msg)
  

@app.route('/crud_libro')
def crud_libro():
    
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accountss WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        
        
        sql = "SELECT * FROM  `lib`;"
        conn= mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)  
        lib=cursor.fetchall() #selecciona registros
        print(lib) #muestra registros
        conn.commit()
        return render_template('crud_libro.html', lib=lib, account = account )

@app.route('/crud_lib')
def crud_lib():
    sql = "SELECT * FROM  `lib`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)  
    lib=cursor.fetchall() #selecciona registros
    print(lib) #muestra registros
    conn.commit()
    return render_template('crud_lib.html', lib=lib )


@app.route('/destroy_1/<int:id_libro>')
def destroy_1(id_libro):
    conn= mysql.connect()
    cursor=conn.cursor()    
    cursor.execute("DELETE FROM lib WHERE id_libro=%s",(id_libro))
    conn.commit()
    return render_template('libros.html')

@app.route('/create_libro')
def create_libro():
    return render_template('libros.html')

# imprimimos la constancia de prestamo 
@app.route('/imprimir')
def imprimir():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accountss WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        
        
        sql = "SELECT * FROM  `lib`;"
        conn= mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)  
        lib=cursor.fetchall() #selecciona registros
        print(lib) #muestra registros
        conn.commit()
        return render_template('imprimir.html', lib=lib, account = account )


# imprimimos la lsita de libros
@app.route('/imprimir_list')
def imprimir_list():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)      
        
    sql = "SELECT * FROM  `libros`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)  
    libros=cursor.fetchall() #selecciona registros
    print(libros) #muestra registros
    conn.commit()
    return render_template('imprimir_list.html', libros=libros)

def librosss():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)      
        
    sql = "SELECT * FROM  `libros`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)  
    libros=cursor.fetchall() #selecciona registros
    print(libros) #muestra registros
    conn.commit()
    return libros

def dato(account):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  

    if 'loggedin' in session:

        cursor.execute('SELECT * FROM accountss WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return account

def pedidos():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT * FROM  `lib`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)  
    lib=cursor.fetchall() #selecciona registros
    print(lib) #muestra registros
    conn.commit()
    return lib
    


@app.route('/download')
def imprimir_librosss():
   
        lib = librosss()
 
        pdf = FPDF()
        pdf.add_page()
        page_width = pdf.w - 2 * pdf.l_margin
        
        pdf.set_font('Arial','B',15)
        pdf.cell(70)
        pdf.cell(50,10,'BIBLIOTECA MYC',1,2, align='C')
        pdf.ln(10);            
        pdf.set_font('Times','B',16.0) 
        pdf.cell(page_width, 0.0, 'LISTA DE LIBROS DE LA BIBLIOTECA MYC', align='C')
        pdf.ln(10)
        
 
        pdf.set_font('Courier', '', 13)
         
        col_width = page_width/4
         
        pdf.ln(1)
         
        th = pdf.font_size

        pdf.set_font('Courier', 'B', 13)

        pdf.cell(col_width, th, 'N', border=1)
        pdf.cell(col_width*2, th, 'LISTA DE LIBROS', border=1)

        pdf.ln(th)
        pdf.set_font('Courier', '', 13)

        for row in lib:
            pdf.cell(col_width, th, str(row[0]), border=1)
            pdf.cell(col_width*2, th, row[1], border=1)
            pdf.ln(th)
         
        pdf.ln(50)
         
        pdf.set_font('Times','',12.0) 
        pdf.cell(page_width, 0.0, 'Gracias por preferir a la BIBLIOTECA DIGITAL  MYC', align='C')
        pdf.ln(6)
        pdf.cell(page_width, 0.0, 'Que tenga un excelente día', align='C')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Lista_Libros.pdf'})


@app.route('/download/pdf')
def imprimir_cons():
        dat = dato('account')
        pedi = pedidos()
 
        pdf = FPDF()
        pdf.add_page()
        page_width = pdf.w - 2 * pdf.l_margin
        pdf.set_font('Arial','B',15)
        pdf.cell(70)
        pdf.cell(50,10,'BIBLIOTECA MYC',1,10, align='C')
        pdf.ln(10);  
        pdf.set_font('Times','B',16.0) 
        pdf.cell(page_width, 0.0, 'constancia de prespamo', align='C')
        pdf.ln(10)
        pdf.set_font('Times','',12.0) 
        pdf.cell(page_width, 0.0, 'la biblioteca digital MYC, por medio de la presente HAGO CONSTAR', align='C')
        pdf.ln(6)
        pdf.cell(page_width, 0.0, 'QUE: se este realizando prestamos de los siguientes libros:', align='C')
        pdf.ln(15)
        
 
        pdf.set_font('Courier', '', 13)
         
        col_width = page_width/4
         
        pdf.ln(1)
         
        th = pdf.font_size

        pdf.set_font('Courier', 'B', 13)

        pdf.cell(col_width*2, th, 'LIBROS', border=1, align='C')
        pdf.cell(col_width*2, th, 'FECHA', border=1, align='C')

        pdf.ln(th)
        pdf.set_font('Courier', '', 13)

        for row in pedi:
           
            pdf.cell(col_width*2, th, row[1], border=1)
            pdf.cell(col_width*2, th, row[2].strftime('%Y-%m-%d'), border=1)
            pdf.ln(th)
        pdf.ln(20)

        ## otro
        
        pdf.set_font('Courier', '', 13)
         
        col_width = page_width/4
         
        pdf.ln(1)
         
        th = pdf.font_size

        pdf.set_font('Courier', 'B', 13)

        pdf.ln(th)
        pdf.set_font('Courier', '', 13)

        for row in dat:
            ##pdf.cell(col_width, th, 'hola')
            ##pdf.cell(col_width*2, th, ro[1])
            pdf.ln(th)
        pdf.ln(10)
         
        pdf.ln(20)
        pdf.set_font('Times','',13.0) 
        pdf.cell(page_width, 0.0, 'Gracias por preferir a la BIBLIOTECA DIGITAL  MYC', align='C')
        pdf.ln(5)
        pdf.cell(page_width, 0.0, 'Que tenga un excelente día', align='C')
        pdf.ln(40)
        pdf.set_font('Times', '', 13)
        pdf.cell(page_width, 0.0, '_______________               _______________', align='C')
        pdf.ln(4)
        pdf.cell(page_width, 0.0, '    prestatario                            prestamista', align='C')
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Constancia_de_prestamo.pdf'})

if __name__ == '__main__':
    app.run(debug=True)

