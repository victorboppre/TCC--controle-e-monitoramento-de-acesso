#main module to manage in Firebase
from firebase import firebase
from datetime import datetime
import time as tm

def new_account(acc,pass1,pass2):
    fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
    request=fb.get('/user',None)
    if(pass1 != pass2):
        return ['senhas diferentes',1]

    elif (acc in request):
        return ['Nome do usuario já utilizado',1]

    else:
        write_nu = fb.put('/user/'+acc,'password',{'password':pass1})
        write_nu = fb.put('/user/'+acc,'salas_ativas',{'salas':'salas'})
        write_nu = fb.put('/user/'+acc,'mestre_salas',{'salas':'salas'})
        return ['Novo usuário '+acc+' criado com sucesso!!!',2]

def login(acc,pass1):
    fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
    request=fb.get('/user',None)
	
    if (acc in request)==False:
        return ['Usuário ou senha inválidos!',2]
	
    login=request[acc]
    login=login['password']
    if (login['password']==pass1):
        return ['Login realizado com sucesso!',1,acc]
    else:
        return ['Usuário ou senha inválidos!',2]

def aar(adm,login, sala, ano, mes, dia, hora, minuto):#add account in a room
    fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
    request=fb.get('/user',None)
    verify = fb.get('/room',None)
    ver_name = fb.get('/room/'+sala+'/mestre',None)
    print(ver_name)
    if (tempo(ano, mes, dia, hora, minuto)) and (login in request) and (sala in verify):
        if ver_name['mestre'] == adm:
            write_nu = fb.put('/user/'+login+'/salas_ativas/',sala,{'ano':ano,'mes':mes,'dia':dia,'hora':hora,'minuto':minuto})
            return ['Operação realizada com sucesso', 1]
        else:
            return ['Usuário não é o administrador da sala!',0]
    else:
        return ['Verificar data e usuário',0]

def add_room(name,acc):
    fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
    request=fb.get('/room',None)
    if name in request:
        return 'sala já utilizada!'
    else:
        fb.put('/room/'+name,'mestre',{'mestre':acc})
        fb.put('/room/'+name,'status',{'status':False})
        fb.put('/room/'+name,'log',{'historico':['inicio']})
        request=fb.get('/user/'+acc+'/mestre_salas',None)
        a=[]
        if(request['salas']== 'salas'):
            a.append(request['salas'])
            a.insert(len(a),name)
            fb.put('/user/'+acc,'mestre_salas',{'salas':a})
        else:
            a=request['salas']
            a.insert(len(a),name)
            fb.put('/user/'+acc,'mestre_salas',{'salas':a})

def use_room(user,room):
    fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
    request = fb.get('/user/'+user+'/salas_ativas',None)
    request1 = fb.get('/room/'+room+'/mestre/',None)
    adm = request1['mestre']
    if (room in request) :
        time = request[room]
        if tempo(time['ano'],time['mes'],time['dia'],time['hora'],time['minuto']):
            log=fb.get('/room/'+room+'/log/historico',None)
            now = datetime.now()
            nl = 'Sala utilizada por '+user+ ' as '+str(now.hour)+':'+str(now.minute)+'--'+str(now.day)+'/'+str(now.month)+'/'+str(now.year)
            log.insert(len(log), nl)
            fb.put('/room/'+room, 'log', {'historico':log})
            fb.put('/room/'+room, 'status', {'status':True})
            tm.sleep(10)
            fb.put('/room/'+room, 'status', {'status':False})
            return 'sala aberta por 10 segundos'
    elif (adm == user):
        log=fb.get('/room/'+room+'/log/historico',None)
        now = datetime.now()
        nl = 'Sala utilizada por '+user+ ' as '+str(now.hour)+':'+str(now.minute)+'--'+str(now.day)+'/'+str(now.month)+'/'+str(now.year)
        log.insert(len(log), nl)
        fb.put('/room/'+room, 'log', {'historico':log})
        fb.put('/room/'+room, 'status', {'status':True})
        tm.sleep(10)
        fb.put('/room/'+room, 'status', {'status':False})
        return 'sala aberta por 10 segundos'

def log_view(acc):
    fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
    request = fb.get('/user/'+acc+'/mestre_salas/salas',None)
    if (request != 'salas'):
        d = []
        for a in request:
            if a != 'salas':
                d.append(a)
        return d
    else:
        return 0

def show_log(room):
    fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
    request = fb.get('/room/'+room+'/log/historico',None)
    return request

def view_user():
    fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
    request = fb.get('/user',None)
    d = []
    for a in request:
        d.append(a)
    return d

def active_rooms(user):
    fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
    request = fb.get('/user/'+user+'/salas_ativas',None)
    d = []
    for a in request:
        if a != 'salas':
            d.append(a)
            
    return d

def tempo(ano, mes, dia, hora, minuto):
	now = datetime.now()
	if((ano > now.year) or (ano >= now.year and mes > now.month) or (ano >= now.year and mes >= now.month and dia > now.day) or (ano >= now.year and mes >= now.month and dia >= now.day and hora > now.hour) or (ano >= now.year and mes >= now.month and dia >= now.day and hora >= now.hour and minuto > now.minute)):
		return True
	else:
		return False
