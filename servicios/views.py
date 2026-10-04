from django.shortcuts import render

def lista_servicios(request):
    servicios_data = [
        {
            'titulo': 'Asesoría Olfativa Personalizada',
            'descripcion': 'Te ayudamos a elegir la fragancia ideal según tus gustos, estilo de vida y ocasión.'
        },
        {
            'titulo': 'Envíos Express a Domicilio',
            'descripcion': 'Despachos seguros en Calbuco y Puerto Montt con seguimiento en tiempo real.'
        },
        {
            'titulo': 'Muestras Gratis en cada Compra',
            'descripcion': 'Incluimos decants de regalo en todos tus pedidos para que pruebes nuevas fragancias.'
        }
    ]
    return render(request, 'servicios/servicios.html', {'servicios': servicios_data})