from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import PostSerializer


class PostListView(APIView):

    def get(self, request):
        cached_posts = cache.get("posts_list")

        if cached_posts is not None:
            return Response(cached_posts)

        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)

        cache.set("posts_list", serializer.data, 60)

        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            cache.delete("posts_list")

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )