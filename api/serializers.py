from rest_framework import serializers 
from main.models import Post 
from main.models import Comment

class PostSerializer(serializers.ModelSerializer):

	class Meta:

		model = Post 
		fields = ('id', 'title', 'content', 'price', 'created_at')

class PostDetailSerializer(serializers.ModelSerializer):

	class Meta:

		model = Post 
		fields = ('id', 'title', 'content', 'price', 'created_at', 'contacts', 'image')


class CommentSerializer(serializers.ModelSerializer):

	class Meta:

		model  = Comment
		fields = ('post', 'author', 'content', 'is_active', 'created_at')

