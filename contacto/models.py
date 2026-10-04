from django.db import models


class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    asunto = models.CharField(max_length=150, blank=True)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.nombre} ({self.email}) - {self.fecha_creacion:%d/%m/%Y}"