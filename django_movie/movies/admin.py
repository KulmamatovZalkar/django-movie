from operator import ge
from django.contrib import admin
from .models import Category, Genre, Movies, Actor, Rating, RatingStars, Reviews, MovieShots
# Register your models here.


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Movies)
admin.site.register(Actor)
admin.site.register(Rating)
admin.site.register(RatingStars)
admin.site.register(Reviews)
admin.site.register(MovieShots)