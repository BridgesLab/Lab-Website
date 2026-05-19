'''This package has the url encodings for the :mod:`papers` app.'''

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from papers.views import PublicationViewSet, JournalClubArticleViewSet

# Create router and register viewsets
router = DefaultRouter()
#   "papers" →  /api/v2/papers/  &  /api/v2/papers/<pk>/
router.register(r'publications', PublicationViewSet, basename='api-publication')
router.register(r'journal-club', JournalClubArticleViewSet, basename='api-journalclub')

urlpatterns = [
    path('', include(router.urls)),
]