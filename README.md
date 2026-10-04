# Parfums D' Parfums

Tienda de perfumes de Calbuco, Chile. Continuación del proyecto de Evaluación 1.

## Aplicaciones

- catalogo: listado público y CRUD de perfumes para administradores.
- nosotros: historia, valores y guía de perfumes.
- contacto: formulario público de consultas y gestión de mensajes en Django Admin.

## Instalación en Windows

Se necesita Python compatible con Django 6.1.1 y PostgreSQL en ejecución.
Crear una base llamada perfumeria desde pgAdmin. Los datos de productos se
gestionan desde Django, no desde pgAdmin.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Editar .env localmente: configurar DB_NAME, DB_USER, DB_PASSWORD, DB_HOST y DB_PORT.
Para generar un SECRET_KEY nuevo:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Pegar el resultado en SECRET_KEY dentro de .env. DEBUG=True es para desarrollo.
En despliegue usar DEBUG=False y configurar ALLOWED_HOSTS. No publicar .env.

```powershell
python manage.py check
python manage.py showmigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Uso

Abrir http://127.0.0.1:8000/ para consultar el catálogo y /nosotros/ para la
información institucional. Ingresar a /admin/ con el superusuario para administrar.
Después de iniciar sesión, el catálogo muestra Agregar perfume, Editar y Eliminar.
Los clientes sin permisos no pueden modificar productos.

Crear al menos tres perfumes desde Django Admin y capturar las operaciones requeridas.
Los datos de ejemplo originales eran Dulce Noche (Femenino, 15000 CLP, 100 ml),
Citrus Fresh (Unisex, 12000 CLP, 50 ml) y Woody Intense (Masculino, 18000 CLP, 100 ml).
No se han cargado automáticamente en PostgreSQL.

## Validaciones y seguridad

Nombre de al menos 3 caracteres; categoría válida; precio y formato mayores que cero.
Un perfume agotado no puede estar destacado. La fecha de creación se controla
desde el sistema. Formularios con CSRF, eliminación solo por POST y confirmación
previa, identificadores inexistentes con respuesta 404 y escritura exclusiva para staff.

## Pruebas

```powershell
python manage.py test catalogo contacto
```

Django crea una base temporal para las pruebas: el usuario PostgreSQL necesita
permiso para crearla. Las 9 pruebas pasaron en una base SQLite aislada en memoria.
Contacto incluye cuatro pruebas adicionales de formulario, validación, campos
protegidos y CSRF. La conexión y las pruebas reales en PostgreSQL siguen pendientes.

## Entrega y equipo

Consultar docs/evaluacion_2.md para justificación, evidencias pendientes y registro de IA.
Entregar informe PDF con capturas reales, resultados y reflexión del equipo.
Cada integrante debe hacer sus propios commits. Integrar main antes de entregar:
la rama de trabajo aún no contiene todos los cambios de contacto.
No subir .env, .venv ni archivos temporales. .env.example contiene solo marcadores.
