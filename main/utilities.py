from django.template.loader import render_to_string 
from django.core.signing import Signer 

from bboard.settings import ALLOWED_HOSTS 

signer = Signer() #Создадим крипто шрифт то есть шифруем

def send_activation_notification(user): #Отправка писем

	if ALLOWED_HOSTS: #Возможные хостинги
		host = 'http://' + ALLOWED_HOSTS[0] #1й хостинг
	else:
		host = 'http://localhost:8000' 
	context = {
		'user': user,
		'host': host,
		'sign': signer.sign(user.username)
	} 
	subject = render_to_string('email/activation_letter_subject.txt', context) #Отправка субьекта
	body_text = render_to_string('email/activation_letter_body.txt', context)  #Отправка писем с подтверждениями
	user.email_user(subject, body_text) 


