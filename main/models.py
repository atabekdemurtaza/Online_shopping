from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):

	is_activated  = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?') #Проверим зарегистрирован ли пользователь
	send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых комментариях?') #Признак того что пользователь уведомлен или нет!

	class Meta(AbstractUser.Meta):

		pass  

#И сразу же зарегистрируем его settings в виде 
"""
	AUTH_USER_MODEL = 'main.User' где User это название класса.
"""

