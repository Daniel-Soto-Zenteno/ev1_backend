from django.urls import path

from . import views

app_name = "contacto"

urlpatterns = [
    path("", views.contacto_view, name="formulario"),
    path("exito/", views.contacto_exito_view, name="exito"),
]