from django.contrib.auth import get_user_model
from django.http import HttpResponseNotAllowed, HttpResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v2.serializers import ArticleSerializer, CommentSerializer
from webapp.models import Article, Comment

from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is None:
            articles = Article.objects.all()
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            article = get_object_or_404(Article, pk=pk)
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_model().objects.last()
        article = serializer.save(author=user)
        return Response({"id": article.id}, status=status.HTTP_201_CREATED)

    def put(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(data=request.data, instance=article)
        if serializer.is_valid():
            article = serializer.save()
            return Response(serializer.data)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        article_id = article.id
        article.delete()
        return Response({"id": article_id}, status=status.HTTP_204_NO_CONTENT)




class CommentView(APIView):
    def get(self, request, article_id, pk=None, *args, **kwargs):
        if pk is None:
            comments = Comment.objects.filter(article_id=article_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            comment = get_object_or_404(Comment, pk=pk, article_id=article_id)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_id, *args, **kwargs):
        article = get_object_or_404(Article, pk=article_id)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_model().objects.last()
        comment = serializer.save(author=user, article=article)
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    def put(self, request, article_id, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk, article_id=article_id)
        serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk, article_id=article_id)
        comment_id = comment.id
        comment.delete()
        return Response({"id": comment_id}, status=status.HTTP_204_NO_CONTENT)