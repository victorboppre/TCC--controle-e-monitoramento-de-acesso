from flask import Flask, render_template, request, session, escape, redirect, url_for
import mqttManager as mqtt
import db_management as db
from PIL import Image
import pyqrcode

app = Flask(__name__)
app.secret_key = '&%82$abcABC2425262728!@$%¨&*('

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/home1/', methods=['POST', 'GET'])
def home1():
    return render_template('index.html')


@app.route('/cadastro/', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        username = request.form['log']
        pass1 = request.form['pass']
        pass2 = request.form['pass2']
        a=db.new_account(username,pass1,pass2)
        return render_template('cadastro.html',msg=a[1],war=a[0])

    else:
        return render_template('cadastro.html',msg=0)

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        pswd = request.form['pswd']
        a=db.login(user,pswd)
        print(a)

        if a[1] == 1:
            session['username']=a[2]


        return render_template('login.html',ms = a[1],warning = a[0])
    else:
        if 'username' in session:
            user = session['username']
            return render_template('index.html',ms = 1)
        
        else:
            return render_template('login.html',ms = 0,warning = 'Usuário conectado')


@app.route('/projeto/', methods=['POST', 'GET'])
def projeto():
    return render_template('projeto.html')

@app.route('/logout/')
def logout():
    print(session['username'])
    session.pop('username', None)
    return redirect('/login/')

@app.route('/log/', methods=['POST', 'GET'])
def log():
    if 'username' in session:
        if request.method == 'POST':
            a = request.form['sala']
            b=db.show_log(a)
            print(b)
            return render_template('log_view1.html',a=a,b=b)


        else:
            user = session['username']
            a=db.log_view(user)
            print(user)
            print(a)
            return render_template('log_view.html',a =a)

    else:
        return redirect('/')

@app.route('/adicionar/', methods=['POST', 'GET'])
def adicionar():
    if 'username' in session:
        if request.method == 'POST':
            user = session['username']
            a = request.form['usuario']
            b = request.form['sala']
            c = request.form['dia']
            d = request.form['mes']
            e = request.form['ano']
            f = request.form['hora']
            g = request.form['minuto']
            h = session['username']
            i = db.active_rooms(user)
            if b in i:
            	db.remove_room(a,b)
            m=db.log_view(user)
            n=db.view_user()
            print(n)
            i=db.aar(h,a,b,int(e),int(d),int(c),int(f),int(g))
            print(i)
            return render_template('adicionar.html',i=i[0],j=i[1],l=i[0], a= m, c= n)
       
        else:
            user = session['username']
            a=db.log_view(user)
            c=db.view_user()
            return render_template('adicionar.html',a =a,c=c)
    else:
        return redirect('/')
@app.route('/QR_code/', methods=['POST', 'GET'])
def qr_code():
    if 'username' in session:
        name = session['username']
        try:
            a = Image.open('static/'+name+'png')
        except:
            new_img = pyqrcode.create(name)
            new_img.png('static/'+name+'.png', scale=8)
            a = '/static/'+session['username']+'.png'
            return render_template('qr.html',a = a)

@app.route('/utilizar/', methods=['POST', 'GET'])
def utilizar():
    if 'username' in session:
        if request.method == 'POST':
            user = session['username']
            try:
                salas = request.form['sala']
            except:
                return render_template('opened.html',a = 3)
            if not(db.use_room(user,salas)):
            	db.remove_room(user,salas)
            	db.log_usage_room(user,salas,"Tempo expiridado:")
            	return render_template('opened.html',a = 2)
            topic2Subscribe = salas + "TCCeletricaEletronica"
            mqtt.set_msg(topic2Subscribe,'open')
            topic2Subscribe += '1'
            a = mqtt.get_msg(topic2Subscribe)
            print('********************')
            print(a)
            if  a == b'Received':
                print('abriu')
                a = 'Sala utilizada por '
                b = 1
            elif a == b"Alreadyo":
                b = 2
                print("sala já aberta")
                return render_template('opened.html',a = b)
            else:
                a = "Sem resposta do módulo, usuário: "
                b = 0
            db.log_usage_room(user,salas,a)
            return render_template('opened.html',a = b)
        else:
            user = session['username']
            salas = db.active_rooms(user)
            return render_template('utilizar.html',a =salas)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
