'''This package has the url encodings for the personnel app.'''

from django.conf.urls import include, url

from personnel import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^$', views.LaboratoryPersonnelList.as_view(), name="laboratory-personnel"),
    url(r'^alumni/?$', views.LaboratoryAlumniList.as_view(), name="laboratory-alumni"),
    url(r'^(?P<name_slug>[\w\d-]+)/$', views.LaboratoryPersonnelDetail.as_view(), name="personnel-details")
]
