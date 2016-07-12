from postbox.models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields=('id','owner','category','c_date')

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Posts
        fields=('id','owner','cid','title','status','image','p_date')

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields=('id','owner','pid','comment','cm_date')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','password','username')

# class RepliesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Replies
#         fields=('cm_id','reply','r_date')
