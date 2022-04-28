from modeltranslation.translator import register, TranslationOptions
from .models import Category, Actor, Movies, Genre, MovieShots

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')



@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movies)
class MoviesTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(MovieShots)
class MovieShotsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')