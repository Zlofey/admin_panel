from django.contrib import admin

from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)

    # Поиск по полям
    search_fields = ('name', 'description', 'id')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'type', 'creation_date', 'rating',)

    # Фильтрация в списке
    list_filter = ('type', 'genres')

    # Поиск по полям
    search_fields = ('title', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)
