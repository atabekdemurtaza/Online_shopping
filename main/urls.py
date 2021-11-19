from django.urls import path 
from .views import index
from .views import other_page
from .views import UserLoginView
from .views import profile

app_name = 'main'
urlpatterns = [

	path('<str:page>/', other_page, name='other_page'),
	path('accounts/login/', UserLoginView.as_view(), name='login'),
	path('accounts/profile/', profile, name='profile'),
	path('', index, name='index'),

]





