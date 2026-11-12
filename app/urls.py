from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_list),
    path("Add/", views.AddUser),
    path("Edit/<id>", views.EditUser),
    path("Delete/<eid>", views.DeleteUser),
    path("View/<eid>", views.ViewUser),
]
