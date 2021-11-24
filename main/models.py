from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):

	is_activated  = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?') #Проверим зарегистрирован ли пользователь
	send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых комментариях?') #Признак того что пользователь уведомлен или нет!

	class Meta(AbstractUser.Meta):

		pass  

#Создадим Рубрику
class Rubric(models.Model):

	name  = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название') #Название
	order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')           #Порядок
	super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Надрубрика') #Надрубрика

#Создадим диспетчер записей
#Он будет выбирать только записи с пустым полем super_rubric
class SuperRubricManager(models.Manager):
	
	#Фильтрация записей
	def get_queryset(self):
		return super().get_queryset().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):

	objects = SuperRubricManager()

	def __str__(self):
		return self.name 

	class Meta:

		proxy        = True
		ordering     = ('order', 'name')
		verbose_name = 'Надрубрика'
		verbose_name_plural = 'Надрубрики'

#Диспетчер записей SubRubricManager будет отбирать лишь записи с непустым полем super_rubric
class SubRubricManager(models.Manager):

	#Фильтрация записей
	def get_queryset(self):
		return super().get_queryset().filter(super_rubric__isnull=False)

class SubRubric(Rubric):

	objects = SubRubricManager()

	def __str__(self):
		return '%s - %s' % (self.super_rubric.name, self.name)

	class Meta:

		proxy = True
		ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
		verbose_name = 'Подрубрика'
		verbose_name_plural = 'Подрубрики'


#И сразу же зарегистрируем его settings в виде 
"""
	AUTH_USER_MODEL = 'main.User' где User это название класса.
"""


