'''URL configuration for the communication API.'''

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from communication.views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='api-post')

urlpatterns = [
    path('', include(router.urls)),
]
