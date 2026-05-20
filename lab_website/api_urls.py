'''Consolidated API v2 URL configuration.

All viewsets are registered on a single router so they appear in the
browsable API root at /api/v2/.
'''

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from papers.views import PublicationViewSet, JournalClubArticleViewSet
from personnel.views import PersonViewSet
from communication.views import PostViewSet

router = DefaultRouter()
router.register(r'publications', PublicationViewSet, basename='api-publication')
router.register(r'journal-club', JournalClubArticleViewSet, basename='api-journalclub')
router.register(r'people', PersonViewSet, basename='api-person')
router.register(r'posts', PostViewSet, basename='api-post')

urlpatterns = [
    path('', include(router.urls)),
]
