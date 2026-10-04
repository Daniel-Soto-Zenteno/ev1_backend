from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalogo.urls')),
    path('nosotros/', include('nosotros.urls')),
    path('contacto/', include('contacto.urls')),
]