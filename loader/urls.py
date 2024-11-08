from django.urls import path

from loader.apps import LoaderConfig
from loader.views import home, items

app_name = LoaderConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("download/", items, name="items"),
]
