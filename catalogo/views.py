from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .forms import PerfumeForm
from .models import Perfume


def lista_perfumes(request):
    perfumes = Perfume.objects.all()
    return render(request, 'catalogo/lista.html', {
        'titulo': 'Catálogo de fragancias',
        'empresa': "Parfums D' Parfums",
        'perfumes': perfumes,
        'total_productos': perfumes.count(),
        'hay_ofertas': perfumes.filter(destacado=True, en_stock=True).exists(),
    })


@staff_member_required
@require_http_methods(['GET', 'POST'])
def perfume_crear(request):
    form = PerfumeForm(request.POST if request.method == 'POST' else None, request.FILES if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfume creado correctamente.')
        return redirect('lista_perfumes')
    return render(request, 'catalogo/perfume_form.html', {'form': form, 'accion': 'Crear'})


@staff_member_required
@require_http_methods(['GET', 'POST'])
def perfume_editar(request, pk):
    perfume = get_object_or_404(Perfume, pk=pk)
    form = PerfumeForm(request.POST if request.method == 'POST' else None, request.FILES if request.method == 'POST' else None, instance=perfume)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfume actualizado correctamente.')
        return redirect('lista_perfumes')
    return render(request, 'catalogo/perfume_form.html', {'form': form, 'accion': 'Editar'})


@staff_member_required
@require_http_methods(['GET', 'POST'])
def perfume_eliminar(request, pk):
    perfume = get_object_or_404(Perfume, pk=pk)
    if request.method == 'POST':
        perfume.delete()
        messages.success(request, 'Perfume eliminado correctamente.')
        return redirect('lista_perfumes')
    return render(request, 'catalogo/perfume_confirmar_eliminar.html', {'perfume': perfume})
