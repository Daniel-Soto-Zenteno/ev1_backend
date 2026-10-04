from django.contrib import admin

from .models import Contacto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "asunto", "fecha_creacion", "atendido")
    list_filter = ("atendido", "fecha_creacion")
    search_fields = ("nombre", "email", "mensaje")
    list_editable = ("atendido",)
    readonly_fields = ("fecha_creacion",)
    ordering = ("-fecha_creacion",)