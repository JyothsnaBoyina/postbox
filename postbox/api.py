from postbox.models import *
from rest_framework.decorators import api_view
from postbox.serializers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework.response import Response


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET', 'POST'])
def user_list(request,format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        lists =User.objects.all()
        list_serializer = UserSerializer(lists, many=True)
        return Response(list_serializer.data)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def category_detail(request, pk,format=None):
    if request.method == 'GET':
        item = Categories.objects.filter(owner_id=pk)
        serializer = CategoriesSerializer(item,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'PUT':
        item = Categories.objects.filter(owner_id=pk)
        serializer = CategoriesSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
       item = Categories.objects.filter(owner_id=pk)
       item.delete()
       return Response(status=204)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def category_detail_view(request, pk,format=None):
    if request.method == 'GET':
        item = Categories.objects.filter(id=pk)
        serializer = CategoriesSerializer(item,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'PUT':
        item = Categories.objects.filter(id=pk)
        serializer = CategoriesSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
       item = Categories.objects.filter(id=pk)
       item.delete()
       return Response(status=204)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def post_detail(request, pk, format=None):
           if request.method == 'GET':
               item = Posts.objects.filter(cid_id=pk)
               serializer = PostsSerializer(item, many=True)
               return Response(serializer.data)

           elif request.method == 'POST':
               # data = JSONParser().parse(request)
               serializer = PostsSerializer(data=request.data)
               if serializer.is_valid():
                   serializer.save()
                   return Response(serializer.data, status=201)
               return Response(serializer.errors, status=400)

           elif request.method == 'PUT':
               item = Posts.objects.filter(cid_id=pk)
               serializer = PostsSerializer(item, data=request.data)
               if serializer.is_valid():
                   serializer.save()
                   return Response(serializer.data)
               return Response(serializer.errors, status=400)

           elif request.method == 'DELETE':
               item = Posts.objects.filter(cid_id=pk)
               item.delete()
               return Response(status=204)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def post_detail_view(request, pk, format=None):
           if request.method == 'GET':
               item = Posts.objects.filter(id=pk)
               serializer = PostsSerializer(item, many=True)
               return Response(serializer.data)

           elif request.method == 'POST':
               # data = JSONParser().parse(request)
               serializer = PostsSerializer(data=request.data)
               if serializer.is_valid():
                   serializer.save()
                   return Response(serializer.data, status=201)
               return Response(serializer.errors, status=400)

           elif request.method == 'PUT':
               item = Posts.objects.filter(id=pk)
               serializer = PostsSerializer(item, data=request.data)
               if serializer.is_valid():
                   serializer.save()
                   return Response(serializer.data)
               return Response(serializer.errors, status=400)

           elif request.method == 'DELETE':
               item = Posts.objects.filter(id=pk)
               item.delete()
               return Response(status=204)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def comment_detail(request, pk, format=None):
                   if request.method == 'GET':
                       item = Comments.objects.filter(pid_id=pk)
                       serializer = CommentsSerializer(item, many=True)
                       return Response(serializer.data)

                   elif request.method == 'POST':
                       # data = JSONParser().parse(request)
                       serializer = CommentsSerializer(data=request.data)
                       if serializer.is_valid():
                           serializer.save()
                           return Response(serializer.data, status=201)
                       return Response(serializer.errors, status=400)

                   elif request.method == 'PUT':
                       item = Comments.objects.filter(pid_id=pk)
                       serializer = CommentsSerializer(item, data=request.data)
                       if serializer.is_valid():
                           serializer.save()
                           return Response(serializer.data)
                       return Response(serializer.errors, status=400)

                   elif request.method == 'DELETE':
                       item = Comments.objects.filter(pid_id=pk)
                       item.delete()
                       return Response(status=204)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def comment_detail_view(request, pk, format=None):
                   if request.method == 'GET':
                       item = Comments.objects.filter(id=pk)
                       serializer = CommentsSerializer(item, many=True)
                       return Response(serializer.data)

                   elif request.method == 'POST':
                       # data = JSONParser().parse(request)
                       serializer = CommentsSerializer(data=request.data)
                       if serializer.is_valid():
                           serializer.save()
                           return Response(serializer.data, status=201)
                       return Response(serializer.errors, status=400)

                   elif request.method == 'PUT':
                       item = Comments.objects.filter(id=pk)
                       serializer = CommentsSerializer(item, data=request.data)
                       if serializer.is_valid():
                           serializer.save()
                           return Response(serializer.data)
                       return Response(serializer.errors, status=400)

                   elif request.method == 'DELETE':
                       item = Comments.objects.filter(id=pk)
                       item.delete()
                       return Response(status=204)
