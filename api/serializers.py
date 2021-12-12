from rest_framework import serializers 
from main.models import Post 

class PostSerializer(serializers.ModelSerializer):

	class Meta:

		model = Post 
		fields = ('id', 'title', 'content', 'price', 'created_at')



