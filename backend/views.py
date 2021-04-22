from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.http import JsonResponse, FileResponse
from . import models, serializers
from django.conf import settings
import os


@api_view(['GET', 'POST', 'PUT'])
def rest_api_user(request, pk=None):
    if request.method == 'GET':
        user = models.User.objects.get(pk=pk)
        serializer = serializers.UserSerializer(user)
        return JsonResponse({'user': serializer.data})

    elif request.method == 'PUT':
        pk = request.data['pk']
        user = models.User.objects.get(pk=pk)
        user.name = request.data.get('name')
        user.email = request.data.get('email')
        user.login == request.data.get('login')
        user.surname = request.data.get('surname')
        user.password = request.data.get('password')
        user.description = request.data.get('description')

        avatar = request.data.get('avatar')
        if avatar != 'undefined':
            directory = f'{settings.MEDIA_ROOT}/users/{pk}'
            if not os.path.exists(directory):
                os.mkdir(directory)
            directory = f'{directory}/avatar'
            if not os.path.exists(directory):
                os.mkdir(directory)

            extension = avatar.name.split('.')[-1]
            user.avatar = f'avatar.{extension}'
            path = f'{directory}/avatar.{extension}'
            with open(path, mode='wb') as file:
                file.write(avatar.file.read())

        user.save()

        return Response(status=status.HTTP_200_OK)

    elif request.method == 'POST':
        login = request.data.get('login')
        password = request.data.get('password')
        if not models.User.objects.filter(
            login=login, password=password).exists():
            user = models.User(**dict(request.data))
            user.save()
            return JsonResponse({'pk': user.pk})            
        return JsonResponse({'pk': 0})


@api_view(['POST', 'GET', 'PUT'])
def rest_api_article(request, pk=None):
    if request.method == 'POST':
        data = dict(request.data)
        pk = int(data.get('pk')[0])
        text = data.get('model')[0]
        title = data.get('title')[0]
        images = data.get('images')
        preview = data.get('preview')[0]
        description = data.get('description')[0]
        user = models.User.objects.get(pk=pk)
        article = models.Article(
            author=user, title=title, text=text,
            description=description, preview=preview)
        article.save()
        article.text = article.text.replace(
            'blob:http://localhost:3000',
            f'http://127.0.0.1:8000/api/articles/{article.pk}/images')

        if preview != 'undefined':
            directory = f'{settings.MEDIA_ROOT}/articles/{article.pk}'
            if not os.path.exists(directory):
                os.mkdir(directory)
            directory = f'{directory}/preview'
            if not os.path.exists(directory):
                os.mkdir(directory)

            extension = preview.name.split('.')[-1]
            article.preview = f'preview.{extension}'
            path = f'{directory}/preview.{extension}'
            with open(path, mode='wb') as file:
                file.write(preview.file.read())

        directory = f'{settings.MEDIA_ROOT}/articles/{article.pk}'
        if not os.path.exists(directory): os.mkdir(directory)
        for image in images:
            path = f'{directory}/{image.name}'
            with open(path, mode='wb') as file:
                file.write(image.file.read())
        article.save()

    if request.method == 'GET':
        article = models.Article.objects.get(pk=pk)
        serializer = serializers.ArticleSerializer(article)
        return JsonResponse({'article': serializer.data})

    if request.method == 'PUT':
        article = models.Article.objects.get(pk=pk)
        article.views = request.data.get('views')
        article.likes = request.data.get('likes')
        article.dislikes = request.data.get('dislikes')
        article.save()


    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def rest_api_image(request, mode=None, pk=None, name=None):
    if request.method == 'POST':
        if mode == 'users':
            pk = request.data.get('pk')
            avatar = request.data.get('avatar')
            extension = str(avatar).split('.')[-1]
            directory = f'{settings.MEDIA_ROOT}/users/{pk}'
            if not os.path.exists(directory):
                os.mkdir(directory)
            user = models.User.objects.get(pk=pk)
            user.avatar = f'avatar.{extension}'
            user.save()
            path = f'{directory}/avatar.{extension}'
            with open(path, mode='wb') as file:
                file.write(avatar.file.read())
    if request.method == 'GET':
        if mode == 'users':
            user = models.User.objects.get(pk=pk)
            path = f'{settings.MEDIA_ROOT}/users/{pk}/avatar/{user.avatar}'
            if os.path.exists(path):
                return FileResponse(open(path, mode='rb'))
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif mode == 'articles':
            article = models.Article.objects.get(pk=pk)
            path = f'{settings.MEDIA_ROOT}/articles/{pk}'
            if name != 'preview': path = f'{path}/{name}'
            else: path = f'{path}/preview/{article.preview}'
            if os.path.exists(path):
                return FileResponse(open(path, mode='rb'))
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def rest_api_articles(request, pk):
    if request.method == 'GET':
        articles = models.Article.objects.filter(author_id=pk)
        serializer = serializers.ArticleMetaSerializer(articles, many=True)
        return JsonResponse({'articles': serializer.data})
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def rest_api_login(request):
    if request.method == 'POST':
        login = request.data.get('login')
        password = request.data.get('password')
        users = models.User.objects.filter(login=login, password=password)
        if users.exists(): return JsonResponse({'pk': users[0].pk})
        else: return JsonResponse({'pk': 0})


@api_view(['GET'])
def get_most_popular(request):
    if request.method == 'GET':
        articles = models.Article.objects.order_by('-views')[:12]
        serializer = serializers.ArticleMetaSerializer(articles, many=True)
        print(len(serializer.data))
        return JsonResponse({'articles': serializer.data})


@api_view(['GET', 'PUT'])
def rest_api_follower(request, author=None, follower=None):
    if request.method == 'PUT':
        author = models.User.objects.get(pk=author)
        follower = models.User.objects.get(pk=follower)
        author.followers.add(follower)
        author.save()
        return JsonResponse({'follow': True})
    if request.method == 'GET':
        author = models.User.objects.get(pk=author)
        follower = models.User.objects.get(pk=follower)
        if follower in author.followers.all():
            return JsonResponse({'follow': True})
        else:
            return JsonResponse({'follow': False}) 


@api_view(['GET'])
def rest_api_followers(request, author):
    if request.method == 'GET':
        author = models.User.objects.get(pk=author)
        serializer = serializers.UserSerializer(
            author.followers, many=True)
        return JsonResponse({'followers': serializer.data})
