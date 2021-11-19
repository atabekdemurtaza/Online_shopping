from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

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


@login_required #Декоратор login_required
def profile(request):

	return render(request, 'main/profile.html')


	