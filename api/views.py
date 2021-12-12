from .serializers import PostSerializer 
from main.models import Post 
from rest_framework.response import Response 
from rest_framework.decorators import api_view 

@api_view(['GET'])
def posts(request):

	if request.method == 'GET':
		post = Post.objects.filter(is_active=True)[:10]
		serializer = PostSerializer(post, many=True)
		return Response(serializer.data)

	