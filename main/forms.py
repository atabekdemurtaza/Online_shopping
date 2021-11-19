from django import forms 
from .models import User 

class ChangeUserInfoForm(forms.ModelForm):

	email = forms.EmailField(required=True, label='Напишите вашу почту') #Поле будет обьязательным


	class Meta:

		model = User 
		fields = ('username', 'email', 'first_name', 'last_name', 'send_messages') #Обьявляем все поля

