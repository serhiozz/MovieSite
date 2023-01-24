from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Movie
from .forms import ReviewForm

# class MoviesView(View):
#     '''Список фильмов'''
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, 'movies/movies.html', {'movie_list': movies})
#
# class MovieDetailView(View):
#     """Полное описание фильма"""
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, 'movies/movie_detail.html', {'movie': movie})

class MoviesView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html' # Можно без этого тега, если насзвать шаблон movie_list (имя модели + list (как класс)
    queryset = Movie.objects.filter(draft=False)
    context_object_name = 'movie_list'

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html' # Можно без этого тега (имя модели + detail (как класс)
    context_object_name = 'movie'
    slug_field = 'url' # Указываем по какому слагу искать, аналог в функции Movie.objects.get(url=slug)

class AddReview(View):
    '''Отзывы'''
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        # if form.is_valid():
        #     form = form.save(commit=False)
        #     form.movie_id = pk
        #     form.save()
        #     или
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()

        return redirect(movie.get_absolute_url())