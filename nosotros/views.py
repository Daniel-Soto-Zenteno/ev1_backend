from django.shortcuts import render


def historia_y_guia(request):
    contexto = {
        'anio_fundacion': 2024,
        'valores': ['Calidad', 'Atención cercana', 'Perfumes réplica'],
        'guia': [
            ('Elige tu estilo', 'Compara aromas frescos, dulces y amaderados para encontrar el que más te guste.'),
            ('Prueba en tu piel', 'Espera unos minutos después de aplicar la fragancia: el aroma puede cambiar con el tiempo.'),
            ('Cuida tu perfume', 'Guarda el frasco lejos del sol y del calor para conservar su aroma.'),
        ],
    }
    return render(request, 'nosotros/nosotros.html', contexto)
