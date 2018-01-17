#main module to manage in Firebase
from firebase import firebase
from datetime import datetime

def new_account(acc,pass1,pass2):
	fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
	request=fb.get('/user',None)
	if(pass1 != pass2):
		return 'senhas diferentes'

	elif (acc in request):
		return 'Nome do usuario já utilizado'

	else:
		write_nu = fb.put('/user',acc,{'password':pass1})
		write_nu = fb.put('/user/'+acc,'salas_ativas',{'salas':'salas'})
		write_nu = fb.put('/user/'+acc,'mestre_salas',{'salas':'salas'})

		return 'Novo usuário '+acc+' criado com sucesso!!!'

def login(acc,pass1):
	fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
	request=fb.get('/user',None)
	
	if (acc in request)==False:
		return 'Usuário ou senha inválidos!'
	
	login=request[acc]
	
	if (login['password']==pass1):
		return 'Login realizado com sucesso!'
	
	else:
		return 'Usuário ou senha inválidos!'

def aar(login, sala, ano, mes, dia, hora, minuto):#add account in a room
	fb=firebase.FirebaseApplication('https://teste-c8737.firebaseio.com/',None)
	request=fb.get('/user',None)
	if (tempo(ano, mes, dia, hora, minuto)) and (login in request):
		write_nu = fb.put('/user/'+login+'/salas_ativas/',sala,{'ano':ano,'mes':mes,'dia':dia,'hora':hora,'minuto':minuto})
		return 'Operação realizada com sucesso'
	else:
		return 'Verificar se as data e usuários são válidos'

def tempo(ano, mes, dia, hora, minuto):
	now = datetime.now()
	if((ano > now.year) or (ano >= now.year and mes > now.month) or (ano >= now.year and mes >= now.month and dia > now.day) or (ano >= now.year and mes >= now.month and dia >= now.day and hora > now.hour) or (ano >= now.year and mes >= now.month and dia >= now.day and hora >= now.hour and minuto > now.minute)):
		return True
	else:
		return False

