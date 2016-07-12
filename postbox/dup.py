# @api_view(['GET', 'POST'])
# def comment_list(request, format=None):
#                    """
#                    List all code snippets, or create a new snippet.
#                    """
#                    if request.method == 'GET':
#                        lists = Comments.objects.all()
#                        list_serializer = CommentsSerializer(lists, many=True)
#                        return Response(list_serializer.data)
#
#                    elif request.method == 'POST':
#                        # data = JSONParser().parse(request)
#                        serializer = CommentsSerializer(data=request.data)
#                        if serializer.is_valid():
#                            serializer.save()
#                            return Response(serializer.data, status=201)
#                        return Response(serializer.errors, status=400)
#
#                # @csrf_exempt
#
#
# @api_view(['GET', 'POST'])
# def post_list(request, format=None):
#            """
#            List all code snippets, or create a new snippet.
#            """
#            if request.method == 'GET':
#                lists = Posts.objects.all()
#                list_serializer = PostsSerializer(lists, many=True)
#                return Response(list_serializer.data)
#
#            elif request.method == 'POST':
#                # data = JSONParser().parse(request)
#                serializer = PostsSerializer(data=request.data)
#                if serializer.is_valid():
#                    serializer.save()
#                    return Response(serializer.data, status=201)
#                return Response(serializer.errors, status=400)
#
#        # @csrf_exempt
#
#
# @api_view(['GET', 'POST'])
# def category_list(request,format=None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         lists =Categories.objects.all()
#         list_serializer = CategoriesSerializer(lists, many=True)
#         return Response(list_serializer.data)
#
#     elif request.method == 'POST':
#         #data = JSONParser().parse(request)
#         serializer = CategoriesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
# #@csrf_exempt
#
#
# #@csrf_exempt
#
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def user_detail(request, pk,format=None):
#     if request.method == 'GET':
#         item = User.objects.filter(id=pk)
#         serializer = UserSerializer(item,many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         #data = JSONParser().parse(request)
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
#     elif request.method == 'PUT':
#         item = User.objects.filter(id=pk)
#         serializer = UserSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#        item = User.objects.filter(id=pk)
#        item.delete()
#        return Response(status=204)
#
