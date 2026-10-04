from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import ContactoForm

@require_http_methods(['GET', 'POST'])
def contacto_view(request):
    form = ContactoForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tu consulta quedó registrada correctamente.')
        return redirect('contacto:contacto_formulario')
    return render(request, 'contacto/contacto_form.html', {'form': form})
