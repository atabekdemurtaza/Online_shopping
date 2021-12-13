from django.urls import path 
from .views import posts 
from .views import PostDetailView
from .views import comments

urlpatterns = [
	
	path('posts/<int:pk>/comments/', comments),
	path('posts/<int:pk>/', PostDetailView.as_view()),
	path('posts/', posts, name='posts'),
]
