from django import forms
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Movies
from .forms import ReviewForm
# Create your views here.


class MovieView(ListView):
    model = Movies
    queryset = Movies.objects.filter(draft=False)
    template_name = 'movies/movies_list.html'
    context_object_name = 'movie_list'


class MovieDetailView(DetailView):
    model = Movies
    slug_field = 'url'


class AddReview(View):
    def post(self, request, pk):
        # form = ReviewForm(request.POST)
        # if form.is_valid():
        #     form = form.save(commit=False)
        #     form.movie_id = pk
        #     form.save()
        form = ReviewForm(request.POST)
        movie = Movies.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()

        return redirect(movie.get_absolute_url())
