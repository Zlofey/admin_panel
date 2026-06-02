from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        return Filmwork.objects.values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type'
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg(
                'personfilmwork__person__full_name',
                distinct=True,
                filter=Q(personfilmwork__role=PersonFilmwork.RoleType.ACTOR),
            ),
            directors=ArrayAgg(
                'personfilmwork__person__full_name',
                distinct=True,
                filter=Q(personfilmwork__role=PersonFilmwork.RoleType.DIRECTOR),
            ),
            writers=ArrayAgg(
                'personfilmwork__person__full_name',
                distinct=True,
                filter=Q(personfilmwork__role=PersonFilmwork.RoleType.WRITER),
            )

        ).order_by('title')

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        def get_next_page(page):
            if page.has_next():
                return page.next_page_number()
            return None

        def get_prev_page(page):
            if page.has_previous():
                return page.previous_page_number()
            return None

        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': get_prev_page(page),
            'next': get_next_page(page),
            'results': list(page)
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.object
