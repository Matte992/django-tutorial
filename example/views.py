from django.http import HttpResponse
from django.shortcuts import render, reverse
from example.models import Movie
from example.models import Genre
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from example.forms import MovieForm, GenreForm
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from example.serializers import MovieSerializer, GenreSerializer, \
    MovieMiniSerializer


# Create your views here.

def hello_world(request):
    return HttpResponse("Hello World!")


def hello_name(request, name):
    return HttpResponse(f'Hello {name}!')


def hello_world_template(request):
    return render(request, "index.html", {})


def simple_list_view(request):
    movies_query = Movie.objects.all()
    return render(request, "list.html", {"movies": movies_query})


class MovieListView(ListView):
    model = Movie
    template_name = "list.html"
    context_object_name = "movies"


class GenreListView(ListView):
    model = Genre
    template_name = "list.html"
    context_object_name = "genres"


class PostCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    success_url = "/movie/add"
    template_name = 'add.html'


class PostEditView(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'add.html'

    @property
    def success_url(self):
        return reverse("movie_list")


class GenreCreateView(CreateView):
    model = Genre
    form_class = GenreForm
    success_url = "/genre/add"
    template_name = 'add.html'


class GenreEditView(UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'add.html'

    @property
    def success_url(self):
        return reverse("genre_list")


class PostDeleteView(DeleteView):
    model = Movie
    template_name = "delete.html"

    @property
    def success_url(self):
        return reverse("movie_list")


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_fields = ("name", "year", "viewed")

    def list(self, request, *args, **kwargs):
        serializer = MovieMiniSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MovieSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def viewed(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.viewed = request.data.get("viewed", True)
        instance.save()
        serializer = MovieSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        serializer = MovieSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        # query_params = self.request.query_params
        queryset = self.queryset

        # year = query_params.get("year")
        # viewed = query_params.get("viewed")

        # if year:
        #    queryset = queryset.filter(year=year)
        # if viewed:
        #    queryset = queryset.filter(viewed=viewed)
        return queryset


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
