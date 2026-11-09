from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .forms import PerfumeForm
from .models import Perfume


def lista_perfumes(request):
    perfumes = Perfume.objects.all()
    busqueda = request.GET.get('q', '').strip()[:120]
    categoria = request.GET.get('categoria', '')
    if categoria not in Perfume.Categoria.values:
        categoria = ''
    ordenes = {
        'nombre': ('nombre', 'pk'),
        'precio_asc': ('precio', 'nombre', 'pk'),
        'precio_desc': ('-precio', 'nombre', 'pk'),
        'recientes': ('-creado', '-pk'),
    }
    orden = request.GET.get('orden', 'nombre')
    if orden not in ordenes:
        orden = 'nombre'
    solo_disponibles = request.GET.get('disponible') == '1'
    if busqueda:
        perfumes = perfumes.filter(nombre__icontains=busqueda)
    if categoria:
        perfumes = perfumes.filter(categoria=categoria)
    if solo_disponibles:
        perfumes = perfumes.filter(en_stock=True)
    perfumes = perfumes.order_by(*ordenes[orden])
    return render(request, 'catalogo/lista.html', {
        'titulo': 'Catálogo de fragancias',
        'empresa': "Parfums D' Parfums",
        'perfumes': perfumes,
        'total_productos': perfumes.count(),
        'busqueda': busqueda,
        'categorias': Perfume.Categoria.choices,
        'categoria_actual': categoria,
        'orden_actual': orden,
        'solo_disponibles': solo_disponibles,
        'filtros_activos': bool(busqueda or categoria or solo_disponibles or orden != 'nombre'),
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
