from django.contrib import messages
from django.shortcuts import redirect, render

from .formulario import ContactoForm


def contacto_view(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "¡Gracias! Tu mensaje fue enviado correctamente. Te contactaremos pronto."
            )
            return redirect("contacto:exito")
    else:
        form = ContactoForm()

    return render(request, "contacto/contacto_form.html", {"form": form})


def contacto_exito_view(request):
    return render(request, "contacto/contacto_exito.html")