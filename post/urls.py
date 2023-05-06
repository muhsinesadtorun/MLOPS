from django.urls import path
from .views import *

app_name = "post"

urlpatterns = [

    path("index/", post_index, name="index"),
    path("<id>/", post_detail, name='detail'),
    path("create/", post_create, name='create'),
    path("<id>/update/", post_update, name="update"),
    path("<id>/delete/", post_delete, name='delete'),
    path("<id>/predict/", post_predict, name='predict'),
]
