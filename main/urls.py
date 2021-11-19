from django.urls import path 
from .views import index
from .views import other_page
from .views import UserLoginView
from .views import profile
from .views import UserLogOutView
from .views import ChangeUserInfoView

app_name = 'main'
urlpatterns = [

	path('<str:page>/', other_page, name='other_page'),
	path('accounts/login/', UserLoginView.as_view(), name='login'),
	path('accounts/logout/', UserLogOutView.as_view(), name='logout'),
	path('accounts/profile/', profile, name='profile'),
	path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
	path('', index, name='index'),

]






