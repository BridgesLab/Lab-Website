'''URL configuration for the personnel API.'''

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from personnel.views import PersonViewSet

router = DefaultRouter()
router.register(r'people', PersonViewSet, basename='api-person')

urlpatterns = [
    path('', include(router.urls)),
]
