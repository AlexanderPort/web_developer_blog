"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', views.rest_api_user),
    path('api/users/login/', views.rest_api_login),
    path('api/users/<int:pk>/', views.rest_api_user),
    path('api/users/<int:author>/followers/', views.rest_api_followers),
    path('api/users/<int:author>/followers/<int:follower>/', views.rest_api_follower),
    path('api/articles/', views.rest_api_article),
    path('api/articles/<int:pk>/', views.rest_api_article),
    path('api/<str:mode>/<int:pk>/images/<str:name>/', views.rest_api_image),
    path('api/users/<int:pk>/articles/', views.rest_api_articles),
    path('api/articles/popular/', views.get_most_popular),
]
