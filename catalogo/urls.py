from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_perfumes, name='lista_perfumes'),
    path('catalogo/crear/', views.perfume_crear, name='perfume_crear'),
    path('catalogo/<int:pk>/editar/', views.perfume_editar, name='perfume_editar'),
    path('catalogo/<int:pk>/eliminar/', views.perfume_eliminar, name='perfume_eliminar'),
]
