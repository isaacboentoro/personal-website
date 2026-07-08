from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("run/", views.run_python, name="run_python"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
]
