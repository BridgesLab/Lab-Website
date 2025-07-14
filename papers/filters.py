"""
Filters for the Papers API using django-filter.

This module provides filtering capabilities for Publication objects
to support the API query parameters.
"""

import django_filters
from django_filters import rest_framework as filters

from papers.models import Publication


class PublicationFilter(filters.FilterSet):
    """
    Filter set for Publication model.
    
    Provides filtering capabilities for:
    - year: Exact year match
    - type: Publication type (exact or contains)
    - laboratory_paper: Boolean filter
    - year_range: Filter by year range (e.g., ?year_after=2020&year_before=2024)
    """
    
    year = django_filters.NumberFilter(field_name='year', lookup_expr='exact')
    year_after = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_before = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
    type = django_filters.CharFilter(field_name='type', lookup_expr='iexact')
    type_contains = django_filters.CharFilter(field_name='type', lookup_expr='icontains')
    laboratory_paper = django_filters.BooleanFilter(field_name='laboratory_paper')
    interesting_paper = django_filters.BooleanFilter(field_name='interesting_paper')
    journal = django_filters.CharFilter(field_name='journal', lookup_expr='icontains')
    
    class Meta:
        model = Publication
        fields = [
            'year',
            'year_after',
            'year_before',
            'type',
            'type_contains',
            'laboratory_paper',
            'interesting_paper',
            'journal',
        ]