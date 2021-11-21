from django.urls import path 
from .views import index
from .views import other_page
from .views import UserLoginView
from .views import profile
from .views import UserLogOutView
from .views import ChangeUserInfoView
from .views import ChangeUserPasswordView
from .views import UserRegisterView, UserRegisterDoneView

app_name = 'main'
urlpatterns = [

	path('<str:page>/', other_page, name='other_page'),
	path('accounts/login/', UserLoginView.as_view(), name='login'),
	path('accounts/logout/', UserLogOutView.as_view(), name='logout'),
	path('accounts/profile/', profile, name='profile'),
	path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
	path('accounts/password/change/', ChangeUserPasswordView.as_view(), name='password_change'),
	path('accounts/register/', UserRegisterView.as_view(), name='register'),
	path('accounts/register/done/', UserRegisterDoneView.as_view(), name='register_done'),
	path('', index, name='index'),

]






