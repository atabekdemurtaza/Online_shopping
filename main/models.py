from django.db import models
from django.contrib.auth.models import AbstractUser 
from .utilities import get_timestamp_path
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField


class User(AbstractUser):

	is_activated  = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?') #Проверим зарегистрирован ли пользователь
	send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых комментариях?') #Признак того что пользователь уведомлен или нет!

	class Meta(AbstractUser.Meta):

		pass  

#Создадим Рубрику
class Rubric(models.Model):

	name  = models.CharField(max_length=40, db_index=True, unique=True, verbose_name='Название') #Название
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


class Post(models.Model):

	rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
	title  = RichTextField(verbose_name='Товар')
	content = models.FloatField(default=0, verbose_name='Цена')
	contacts = models.TextField(verbose_name='Контакты')
	image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
	is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке ?')
	created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

	#В переопределенном отделе(методе) delete() перед удалением текущей
	#записи мы перебираем и вызовем метода delete() и удаляем все 
	#связанные дополнительные иллюстрации
	def delete(self, *args, **kwargs):

		for ai in self.additionalimage_set.all():
			ai.delete()
		super().delete(*args, **kwargs)

	class Meta:

		verbose_name_plural = 'Обьявления'
		verbose_name = 'Обьявление'
		ordering = ['-created_at']