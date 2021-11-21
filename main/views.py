from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView 
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import User 
from .forms import ChangeUserInfoForm
from django.contrib.auth.views import PasswordChangeView

def index(request):

	return render(request, 'main/index.html')

def other_page(request, page):

	try:
		template = get_template('main/' + page + '.html') #получаем page Если процесс успешно
	except TemplateDoesNotExist: #Если страница не найдена то появится отшибка 
		raise Http404            #Тут сразу мигом захватываем запрос
	return HttpResponse(template.render(request=request)) #И отправляем запрос


class UserLoginView(LoginView):

	template_name = 'main/login.html' #Указываем путь к файлу для входа


@login_required #Декоратор login_required потребуется для проверки если пользователь вошел тогда сработает 
def profile(request):

	return render(request, 'main/profile.html')

class UserLogOutView(LogoutView, LoginRequiredMixin): #Проверим если пользователь уже существует внутри сайта. То он может выйти с сайта.

	template_name = 'main/logout.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):

	model = User 
	template_name = 'main/change_user_info.html'
	form_class = ChangeUserInfoForm 
	success_url = reverse_lazy('main:profile')
	success_message = 'Данные пользователя изменены'

	def setup(self, request, *args, **kwargs):

		self.user_id = request.user.pk 
		return super().setup(request, *args, **kwargs)

	def get_object(self, queryset=None):

		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk=self.user_id)

#Поле когда пользователь хочет изменить свой пароль 
class ChangeUserPasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):

	template_name = 'main/password_change.html'
	success_url   = reverse_lazy('main:profile')
	success_message  = 'Пароль изменен'


