from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import ArticleListSerializer, CommentSerializer, ArticleSerializer, ReplySerializer
from .models import Article, Comment, Reply

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list_create(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    else:
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE', 'PUT'])
# @permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        

@api_view(['GET'])
def comment_list(request):
    if request.method == 'GET':
        comments = get_list_or_404(Comment)
        # print(comments)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['POST'])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    print(article)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def reply_list(request):
    if request.method == 'GET':
        replys = get_list_or_404(Reply)
        serializer = ReplySerializer(replys, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def reply_detail(request, reply_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)

    if request.method == 'GET':
        serializer = ReplySerializer(reply)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CommentSerializer(reply, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['POST'])
def reply_create(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    serializer = ReplySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(comment=comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def article_likes(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    likes = article.likes.all()
    
    if likes.filter(pk=request.user.pk).exists():
        article.likes.remove(request.user)  
    else:
        article.likes.add(request.user) 
    
    updated_likes = ArticleSerializer(article)
    
    return Response(updated_likes.data, status=status.HTTP_200_OK) 
    