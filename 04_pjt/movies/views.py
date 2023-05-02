from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.decorators.http import require_safe
from .models import Movie, Genre
from .forms import MovieForm

# Create your views here.
@require_safe
def index(request):
    movies = get_list_or_404(Movie)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie' : movie,
    }
    return render(request, 'movies/detail.html', context)

@require_safe
def recommended(request, name):
    print(name)
    movies = get_list_or_404(Movie)
    li = []
    i=0
    for movie in movies:
        for genre in movie.genres.all():
            if genre.name == name:
                i += 1
                li.append(get_object_or_404(Movie, pk=movie.pk))
        if i == 10:
            break
    context = {
        'movies' : movies,
        'name' : name,
        'li' : li,
    }
    return render(request, "movies/recommended.html", context)


@require_safe
def genre_list(request):
    return render(request, "movies/genre_list.html")
