from .serializers import PostSerializer 
from main.models import Post 
from rest_framework.response import Response 
from rest_framework.decorators import api_view 
from rest_framework.generics import RetrieveAPIView
from .serializers import PostDetailSerializer
from rest_framework.decorators import permission_classes 
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from main.models import Comment
from .serializers import CommentSerializer

@api_view(['GET'])
def posts(request):

	if request.method == 'GET':
		post = Post.objects.filter(is_active=True)[:10]
		serializer = PostSerializer(post, many=True)
		return Response(serializer.data)

class PostDetailView(RetrieveAPIView):

	queryset = Post.objects.filter(is_active=True)
	serializer_class = PostDetailSerializer

#Добавим и комменты в API
@api_view(['GET','POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):

	if request.method == 'POST':
		serializer = CommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
	else:
		comments = Comment.objects.filter(is_active=True, post=pk)
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data)