from django.conf.urls import url
from apps.schema import views

urlpatterns=[
    url(r'^(?P<table>\w+)/$', views.schema),
    url(r'^$', views.schema),
]



