from email import message
from django import forms

from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Genre, Movies, Actor, Rating, RatingStars, Reviews, MovieShots
# Register your models here.
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MoviesAdminForm(forms.ModelForm):
    description = forms.CharField(
        label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movies
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("id", "name", "url")


# class ReviewsInline(admin.TabularInline):
#     model = Reviews
#     extra = 0

class ReviewsInline(admin.StackedInline):
    model = Reviews
    extra = 0
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.StackedInline):
    model = MovieShots
    extra = 0
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100%"/>')

    get_image.short_description = "Photo of actor"


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "get_image", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewsInline]
    actions = ['published', 'unpublish']
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    form = MoviesAdminForm
    readonly_fields = ("get_image",)
    # fields = (('actors', "director", "genres"),)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster", "get_image")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (('actors', "director", "genres", "category"),)
        }),
        (None, {
            "fields": (('budget', "fees_in_use", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (('url', "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="100%"/>')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'

        self.message_user(request, f'{message_bit}')

    def published(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'

        self.message_user(request, f'{message_bit}')

    published.short_description = "Опубликовать"
    published.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Poster"


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="50" height="100%"/>')

    get_image.short_description = "Photo of actor"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="100%"/>')

    get_image.short_description = "Photo of actor"


# admin.site.register(Category, CategoryAdmin)
admin.site.register(RatingStars)


admin.site.site_title = "Django Movies"
admin.site.site_header = "Dajngo Movies"
