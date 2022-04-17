from django.urls import reverse
from django.db import models
from datetime import date
# Create your models here.


class Category(models.Model):
    """Category"""

    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """Actor and directors"""
    name = models.CharField("Имя", max_length=150)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    photo = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актёры и режиссёры"
        verbose_name_plural = "Актёры и режиссёры"


class Genre(models.Model):
    """Genre"""

    name = models.CharField("Жанры", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movies(models.Model):
    """Movies"""

    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100)
    description = models.TextField("Описание")
    poster = models.ImageField("Изображение", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2022)
    country = models.CharField("Страна", max_length=30)
    director = models.ManyToManyField(
        Actor, verbose_name="Режиссер", related_name="film_director")
    actors = models.ManyToManyField(
        Actor, verbose_name="Актёры", related_name="film_actors")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    world_premiere = models.DateField("Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField(
        "Бюджет", default=0, help_text="Указывать сумму в долларах")
    fees_in_use = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="Указывать сумму в долларах")
    fees_in_world = models.PositiveIntegerField(
        "Сборы в Мире", default=0, help_text="Указывать сумму в долларах")
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull = True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображения", upload_to="movie_shots/")
    movie = models.ForeignKey(
        Movies, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадры из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStars(models.Model):
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Звезды рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating(models.Model):
    ip = models.CharField("IP", max_length=15)
    star = models.ForeignKey(
        RatingStars, on_delete=models.CASCADE, verbose_name="Звезды")
    movie = models.ForeignKey(
        Movies, on_delete=models.CASCADE, verbose_name="Фильмы")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинг"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(
        Movies, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
