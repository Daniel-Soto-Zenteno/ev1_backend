from django.shortcuts import render

def lista_perfumes(request):
    contexto = {
        'titulo': 'Catálogo de Fragancias',
        'empresa': 'Parfums D\' Parfums',
        'hay_ofertas': True,
        'total_productos': 3,
        'perfumes': [
            {
                'nombre': 'Perfume Dulce Noche',
                'categoria': 'Femenino',
                'precio': 15000,
                'ml': 100,
                'en_stock': True,
                'destacado': True
            },
            {
                'nombre': 'Citrus Fresh',
                'categoria': 'Unisex',
                'precio': 12000,
                'ml': 50,
                'en_stock': True,
                'destacado': False
            },
            {
                'nombre': 'Woody Intense',
                'categoria': 'Masculino',
                'precio': 18000,
                'ml': 100,
                'en_stock': False,
                'destacado': False
            },
        ]
    }
    return render(request, 'catalogo/lista.html', contexto)