from django.contrib import admin

from .models import Perfume


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'ml', 'en_stock', 'destacado']
    list_filter = ['categoria', 'en_stock', 'destacado']
    search_fields = ['nombre']
    readonly_fields = ['creado']
