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
from django.views.generic.edit import CreateView 
from .forms import RegisterUserForm
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature 
from .utilities import signer 
from django.views.generic.edit import DeleteView 
from django.contrib.auth import logout 
from django.contrib import messages
from django.core.paginator import Paginator 
from django.db.models import Q 
from .models import SubRubric, Post 
from .forms import SearchForm
from django.shortcuts import redirect
from .forms import PostForm, AIFormSet
from .models import Comment
from .forms import UserCommentForm
from .forms import GuestCommentForm



def index(request):

	posts = Post.objects.filter(is_active=True)[:10]
	#Это поля для поиска. Поиск ведется либо с title или content
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']
		q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
		posts = posts.filter(q)
	else:
		keyword = ''
	form = SearchForm(initial={'keyword': keyword})
	paginator = Paginator(posts, 2)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1 
	page = paginator.get_page(page_num)
	context = {
		'posts': posts,
		'form' : form,
		'page' : page,
	}
	return render(request, 'main/index.html', context)

def other_page(request, page):

	try:
		template = get_template('main/' + page + '.html') #получаем page Если процесс успешно
	except TemplateDoesNotExist: #Если страница не найдена то появится отшибка 
		raise Http404            #Тут сразу мигом захватываем запрос
	return HttpResponse(template.render(request=request)) #И отправляем запросq


class UserLoginView(LoginView):

	template_name = 'main/login.html' #Указываем путь к файлу для входа


@login_required #Декоратор login_required потребуется для проверки если пользователь вошел тогда сработает 
def profile(request):

	#Пользователи будут посматривать своих обьявлений, добавлять, править и удалять обьявления.
	posts = Post.objects.filter(author=request.user.pk)
	context = {
		'posts': posts
	}
	return render(request, 'main/profile.html', context)

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

#Создадим поле регистрации
class UserRegisterView(CreateView):

	template_name = 'main/register_user.html' #имя шаблона
	model = User                              #База
	form_class = RegisterUserForm             #Форма
	success_url = reverse_lazy('main:register_done') #И новая страница после регистрации 

#Создадим поле успешности после активации
class UserRegisterDoneView(TemplateView):

	template_name = 'main/register_done.html'

#Создадим контроллер для активации пользователя 
def user_activate(request, sign):

	try:
		username = signer.unsign(user) 
	except BadSignature:
		return render(request, 'main/bad_signature.html')
	user = get_object_or_404(User, username=username)
	if user.is_activated:
		template = 'main/user_is_activated.html'
	else:
		template = 'main/activation_done.html'
		user.is_active = True 
		user.is_activated = True 
		user.save()
	return render(request, template)


#Создадим класс для удалении пользователя
class DeleteUserView(LoginRequiredMixin, DeleteView):

	model = User 
	success_url = reverse_lazy('main:index')
	template_name = 'main/delete_user.html'

	#Сохранили текущий ключ пользователя
	def setup(self, request, *args, **kwargs):

		self.user_id = request.user.pk 
		return super().setup(request, *args, **kwargs)

	#Создаем всплывающее сообщение об успешном удалении пользователя
	def post(self, request, *args, **kwargs):

		logout(request)
		messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
		return super().post(request, *args, **kwargs)

	#Отыскаем ключ пользователя, подлежащего удалению 
	def get_object(self, queryset=None):

		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk=self.user_id)

#Обьявим рубрик из БД
def by_rubric(request, pk):

	rubric = get_object_or_404(SubRubric, pk=pk)
	posts  = Post.objects.filter(is_active=True, rubric=pk)
	#Это поля для поиска. Поиск ведется либо с title или content
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']
		q = Q(title__icontains=keyword) 
		posts = posts.filter(q)
	else:
		keyword = ''
	form = SearchForm(initial={'keyword': keyword})

	paginator = Paginator(posts, 10)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1 
	page = paginator.get_page(page_num)
	context = {
		'rubric':rubric,
		'page': page,
		'posts': page.object_list,
		'form': form
	}
	return render(request, 'main/by_rubric.html', context)
#Пост для общего пользования
def detail(request, rubric_pk, pk):

	#Старая версия
	"""post = get_object_or_404(Post, pk=pk)
	ais = post.additionalimage_set.all()
	context = {
		'post':post,
		'ais' :ais,
	}
	return render(request, 'main/detail.html', context)"""

	#Новая версия с комментариями
	post = Post.objects.get(pk=pk) #В поле post заносим ключ вывод на странице обьявления
	ais  = post.additionalimage_set.all()
	comments = Comment.objects.filter(post=pk, is_active=True)
	initial = {
		'post': post.pk
	}
	if request.user.is_authenticated: #Если пользователь вошел в систему
		initial['author'] = request.user.username #Заносим туда имя пользователя
		form_class = UserCommentForm #Если выполнил то может оставлять коммент
	else:
		form_class = GuestCommentForm #Если не пользователь то оставляет как гость
	form = form_class(initial=initial) #Обьект формы сохраним в переменной с именем form.Форма из этой переменной впоследствии будет выведена на странице сведений об обьявлении.
	if request.method == 'POST':
		c_form = form_class(request.POST) #Пользователь оставил коммент мы сохраняем его тут
		if c_form.is_valid(): #Проверяем валидацию вторго форма
			c_form.save()     #Если соответствует то сохраним
			messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
		else:
			form = c_form 
			messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
	context = {
		'post': post,
		'ais' : ais,
		'comments': comments,
		'form': form
	}
	return render(request, 'main/detail.html', context)

#Пост для зарегистрированных пользователей
@login_required
def profile_post_detail(request, rubric_pk, pk):

	post = get_object_or_404(Post, pk=pk)
	ais = post.additionalimage_set.all()
	posts = Post.objects.filter(author=request.user.pk)
	context = {
		'post': post,
		'ais': ais,
		'posts':posts,
	}
	return render(request, 'main/profile_post_detail.html', context)

#Добавим обьявление, реализуем в виде функции(в виде класса его реализовать будет сложнее) так как назовем его profile_post_add()
@login_required
def profile_post_add(request):

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save()
			formset = AIFormSet(request.POST, request.FILES, instance=post)
			if formset.is_valid():
				formset.save()
				messages.add_message(request, messages.SUCCESS, 'Обьявление добавлено')
				return redirect('main:profile')
	else:
		form = PostForm(initial={'author':request.user.pk})
		formset = AIFormSet()
	context = {
		'form': form, 
		'formset': formset
	}
	return render(request, 'main/profile_post_add.html', context)

#Здесь нужно отметить что у нас имеются 3 важных момента.1х при создании формы перед выводом страницы сохранения мы заносим в поле autor
#ормы ключ текущего пользователя, который станет автором обьявления.
#Во-вторых во время сохраниения введенного обьявления, при создании обьектов формы набора и набора форм, мы должны передать контсрукторам их
#класса вторым позиционным параметром словарь со всеми полученными файлами(он хранится в атрибуте FILES обьекта запроса). Если мы не сделаем
#этого, то отправленные пользователем илююстрации окажутся потерянными.

#Для зарегистрированных пользователей
#Пользователь умеет правку поста
@login_required
def profile_post_change(request, pk):

	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save()
			formset = AIFormSet(request.POST, request.FILES, instance=post)
			if formset.is_valid():
				formset.save()
				messages.add_message(request, messages.SUCCESS, 'Обьявление исправлено')
				return redirect('main:profile')
	else:
		form = PostForm(instance=post)
		formset = AIFormSet(instance=post)
	context = {
		'form' : form,
		'formset' : formset
	}
	return render(request, 'main/profile_post_change.html', context)

#Для зарегистрированных пользователей
#Пользователь умеет удалить пост
@login_required
def profile_post_delete(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		post.delete()
		messages.add_message(request, messages.SUCCESS, 'Обьявление удалено')
		return redirect('main:profile')
	else:
		context = {
			'post': post
		}
		return render(request, 'main/profile_post_delete.html', context)

