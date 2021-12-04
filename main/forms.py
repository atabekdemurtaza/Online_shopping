from django import forms
from django.db.models import fields 
from .models import User 
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .apps import user_registered
from .models import SuperRubric, SubRubric
from django.forms import inlineformset_factory, widgets
from .models import Post, AdditionalImage

class ChangeUserInfoForm(forms.ModelForm):

	email = forms.EmailField(required=True, label='Напишите вашу почту') #Поле будет обьязательным


	class Meta:

		model = User 
		fields = ('username', 'email', 'first_name', 'last_name', 'send_messages') #Обьявляем все поля


#Создадим форму регистрации 

class RegisterUserForm(forms.ModelForm):

	email 	   = forms.EmailField(required=True, label='Почта')
	password_1 = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
	password_2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput, help_text='Повторите пароль еще раз')

	#Напишем валидацию 1-ого пароля
	def clean_password_1(self):

		password_1 = self.cleaned_data['password_1']
		if password_1:
			password_validation.validate_password(password_1)
		return password_1

	#Сравниваем 2 пароля
	def clean(self):

		super().clean()
		password_1 = self.cleaned_data['password_1']
		password_2 = self.cleaned_data['password_2']
		if password_1 and password_2 and password_1 != password_2:
			errors = {
				'password_2': ValidationError('Введенные пароли не совпадают', code='password_dismatch')
			}
			raise ValidationError(errors)

	#Сохраняем пользователя 
	def save(self, commit=True):

		user = super().save(commit=False) #После регистрации пользователь должен активировать 
		user.set_password(self.cleaned_data['password_1']) #Он введет пароль
		user.is_active = False  #До тех новый пользователь будет неактивным пока не делает активацию
		user.is_activated = False  #Тоже самое 
		if commit:           #Если он подтверден то активация успешно
			user.save()      #И сохраняем нью пользователя
		user_registered.send(RegisterUserForm, instance=user) #После него отправляем сигнал 
		return user 

	#Создадим форму
	class Meta:

		model = User 
		fields = ('username', 'email', 'password_1', 'password_2', 'first_name', 'last_name', 'send_messages')

#Создадим класс SubRubricAdmin
class SubRubricForm(forms.ModelForm):

	super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(), empty_label=None, label='Надрубрика', required=True)

	class Meta:

		model = SubRubric
		fields = '__all__'

class SearchForm(forms.Form):

	#Пока посетитель может ввести в поле keyword искомое слово
	#а может и не ввести(чтобы отменить выполненный поиск и вновь)
	keyword = forms.CharField(required=False, max_length=20, label='')

#Обьявим форму PostForm, связанную с моделью Post, для ввода самого обьявления и встроеннуй набор форм AIFormSet
class PostForm(forms.ModelForm):

	class Meta:

		model = Post 
		fields = '__all__'
		widgets = {
			'author': forms.HiddenInput
		}

AIFormSet = inlineformset_factory(Post, AdditionalImage, fields='__all__')
