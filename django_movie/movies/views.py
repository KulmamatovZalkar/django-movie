from multiprocessing import context
from urllib import request
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from .models import Movies, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm
from django.db.models import Q
# Create your views here.


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        # return Movies.objects.filter(draft=False).values_list("year")
        return Movies.objects.filter(draft=False).values("year")


class MovieView(GenreYear, ListView):
    model = Movies
    queryset = Movies.objects.filter(draft=False)
    template_name = 'movies/movies_list.html'
    context_object_name = 'movie_list'
    paginate_by = 2


class MovieDetailView(GenreYear, DetailView):
    model = Movies
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context


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


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    paginate_by = 1

    def get_queryset(self):
        queryset = Movies.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) | Q(genres__in=self.request.GET.getlist("genre")))
        return queryset
    context_object_name = 'movie_list'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join(
            [f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join(
            [f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = Movies.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    context_object_name = 'movie_list'

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            print(ip)
        else:
            ip = request.META.get('REMOTE_ADDR')
            print(ip)
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movies")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 3
    template_name = 'movies/movies_list.html'
    context_object_name = 'movie_list'

    def get_queryset(self):
        return Movies.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context