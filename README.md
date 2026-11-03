# Parfums D’ Parfums

Aplicación de una perfumería de Calbuco, Chile, desarrollada con Django y PostgreSQL. Conserva el catálogo HTML, su CRUD administrativo, Nosotros, Contacto y Servicios. La evaluación 3 agrega una API REST al modelo existente `Perfume`, usando la misma base de datos.

Integrantes: Daniel Soto, Diego Villota y Mauro Sotomayo.

## Instalación local en Windows

Requisitos: Python compatible con las versiones de `requirements.txt`, PostgreSQL en ejecución y una base de datos creada para el proyecto. La instalación actual se verificó con Python 3.14 y PostgreSQL 18.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Copiar `.env.example` solo en una instalación nueva: conservar el `.env` si ya existe. Configurar localmente `SECRET_KEY` (aleatoria), `DEBUG`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT`. El usuario de PostgreSQL debe poder acceder a esa base. Nunca publicar `.env` ni contraseñas reales.

```powershell
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Sitio: http://127.0.0.1:8000/ — administración: http://127.0.0.1:8000/admin/.
Los usuarios se crean localmente; no hay una contraseña compartida. Para probar las escrituras de la API usar un usuario activo con `is_staff=True` (un superusuario cumple esta condición). Un usuario activo sin ese permiso permite comprobar el rechazo 403.

## API REST: política de acceso

Todas las consultas de la API requieren JWT. Crear, modificar o eliminar requiere además un usuario administrador (`is_staff=True`), como en el CRUD HTML. El catálogo HTML sigue siendo público; las sesiones del sitio no sustituyen el token de la API.

| Método | Ruta | Resultado | Acceso |
|---|---|---|---|
| POST | `/api/token/` | Access y refresh, 200 | Usuario y contraseña válidos |
| POST | `/api/token/refresh/` | Access renovado, 200 | Refresh válido |
| GET | `/api/perfumes/` | Lista JSON, 200 | JWT |
| GET | `/api/perfumes/<id>/` | Registro JSON, 200 | JWT |
| POST | `/api/perfumes/` | Registro creado, 201 | JWT + administrador |
| PUT | `/api/perfumes/<id>/` | Reemplazo de campos editables, 200 | JWT + administrador |
| PATCH | `/api/perfumes/<id>/` | Actualización parcial, 200 | JWT + administrador |
| DELETE | `/api/perfumes/<id>/` | Eliminado, 204 sin cuerpo | JWT + administrador |

Obtener tokens enviando JSON con `username` y `password` a `/api/token/`. En las siguientes solicitudes enviar `Authorization: Bearer <access>`. Access dura 15 minutos y refresh un día.

Ejemplo de cuerpo JSON para POST o PUT:

```json
{
  "nombre": "Citrus Fresh",
  "categoria": "Unisex",
  "precio": "12000",
  "ml": 50,
  "en_stock": true,
  "destacado": false
}
```

Campos: `nombre`, `categoria`, `precio` y `ml` obligatorios; `en_stock`, `destacado` e `imagen` opcionales. `id` y `creado` son de solo lectura. Para imágenes enviar multipart/form-data en lugar de JSON.

Las validaciones del serializer incluyen nombre de al menos tres caracteres, precio y ml positivos, categoría permitida y la regla de no destacar perfumes sin stock. PATCH comprueba también el estado existente del objeto. El modelo permite nombres repetidos: no declara unicidad, por lo que no se añade una restricción ajena al negocio.

Errores: 400 con errores por campo; 401 con `detail` para token ausente/inválido/vencido; 403 con `detail` para usuarios sin permiso de escritura; 404 con `detail` si no existe el identificador. Un POST exitoso devuelve el registro creado, incluido su `id`.

## Organización y configuración

- `catalogo/models.py`: modelo existente y reglas del negocio.
- `catalogo/serializers.py`: conversión a JSON, validación de campos y ejecución de la regla `clean()` del modelo.
- `catalogo/api.py`: `ModelViewSet` que consulta y modifica mediante el ORM; permisos según la operación.
- `config/urls.py`: router `/api/perfumes/` y rutas de tokens.
- `config/settings.py`: DRF registrado, autenticación JWT, JSON y permisos globales; PostgreSQL y secretos mediante variables de entorno.

El router expone las rutas REST sin sustituir las rutas HTML. El viewset reutiliza `Perfume` y la configuración PostgreSQL actual; no crea otra tabla ni necesita migraciones nuevas.

## Verificación y evidencias

```powershell
python manage.py test catalogo contacto config --noinput
python manage.py showmigrations --plan
python manage.py makemigrations --check --dry-run
python -m pip check
```

Las pruebas necesitan un usuario PostgreSQL que pueda crear la base de pruebas. Django crea y elimina su base `test_<DB_NAME>`; no ejecutar contra una base de pruebas preexistente con información que se deba conservar.

Resultado local del 03-11-2026: 35 pruebas aprobadas sobre PostgreSQL, sin migraciones pendientes ni dependencias rotas. Incluye JWT, API, CRUD HTML y contacto.

Importar `docs/api_perfumes.postman_collection.json` en Postman. Configurar las variables de la colección `base_url`, `username` y `password` solo localmente y usar un administrador de pruebas. Ejecutar en orden con el servidor encendido; la colección crea y elimina un perfume de demostración y conserva los tokens solo en las variables locales de Postman. No compartir/exportar valores reales de credenciales o tokens. Capturar los resultados con esos valores ocultos para el informe.

Revisión de cumplimiento y pendientes: [Evaluación 3](docs/evaluacion_3.md). Las pruebas automáticas y la colección no sustituyen las capturas y el informe exigidos por la pauta.
