"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers

from example.views import hello_world, hello_name, hello_world_template, \
    simple_list_view, MovieListView, GenreListView, PostCreateView, \
    PostEditView, GenreCreateView, GenreEditView, PostDeleteView, MovieViewSet, \
    GenreViewSet

router = routers.DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"genres", GenreViewSet)

urlpatterns = [
    path("hello/", hello_world, name='hello_world'),
    path("hello/<str:name>/", hello_name),
    path('admin/', admin.site.urls),
    path('hello_template/', hello_world_template, name='hello_world_template'),
    path('simple_list/', simple_list_view),
    path('movie_list_by_class_view/', MovieListView.as_view(),
         name="movie_list"),
    path('genre_list_by_class_view/', GenreListView.as_view(),
         name="genre_list"),
    path('movie/add/', PostCreateView.as_view(),
         name="movie_add"),
    path('movie/edit/<int:pk>/', PostEditView.as_view(),
         name="movie_edit"),
    path('genre/add/', GenreCreateView.as_view(),
         name="genre_add"),
    path('genre/edit/<int:pk>/', GenreEditView.as_view(),
         name="genre_edit"),
    path('movie/delete/<int:pk>/', PostDeleteView.as_view(),
         name="delete_view"),
    # (...),
    # django rest framework
    path("api-auth/", include("rest_framework.urls")),
    path("", include(router.urls)),
    # path("api-token-auth/", views.obtain_auth_token)
]
