from django.urls import path
from . import views

app_name = 'contacto'
urlpatterns = [
    path('exito/', views.contacto_exito_view, name='exito'),
    path('', views.contacto_view, name='contacto_formulario'),
    path('', views.contacto_view, name='formulario'),
]
