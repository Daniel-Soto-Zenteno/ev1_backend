# Revisión de la evaluación 3 — 03-11-2026

Fuente: pauta local `Evaluacion_3_API_RESTful_Django.pdf`, especialmente secciones 4, 5, 6, 8, 9 y rúbrica 11. Se aplicó esta pauta porque la rama actual es `feature/api-rest` y ya contenía DRF, JWT y serializer. La evaluación 2 es el antecedente del sitio HTML.

## Punto 5: implementado y verificado

Recurso: `Perfume`, de `catalogo`, reutilizando su modelo, tabla y PostgreSQL actuales.

- Listado y detalle GET: 200 JSON con JWT obligatorio.
- Creación POST: 201 JSON con el registro persistido.
- Edición completa PUT y parcial PATCH: 200 JSON y persistencia.
- Eliminación DELETE: 204 sin cuerpo, registro eliminado.
- Datos inválidos: 400 y errores JSON por campo.
- Token ausente, inválido, vencido o usuario inactivo: 401.
- Usuario autenticado sin `is_staff`: 403 en todas las escrituras.
- Identificador inexistente: 404 JSON.
- `id` y `creado`: solo lectura.
- Validaciones obligatorias, tipos, rangos y reglas propias del modelo, incluso en PATCH.
- No se impone unicidad al nombre, porque el modelo no la requiere.
- La autenticación de sesión del sitio no autoriza escrituras de la API.

Archivos agregados: `catalogo/api.py`, `catalogo/test_api.py` y colección Postman. Ruta registrada mediante router en `config/urls.py`. No se modificó el modelo ni se generaron migraciones.

## Revisión de todos los criterios

| Criterio | Puntos | Estado comprobado | Pendiente para la entrega |
|---|---:|---|---|
| Configuración técnica | 15 | DRF y JWT registrados; dependencias instaladas y consistentes; conexión real a PostgreSQL 18.6 en base local `parfums`; `.env` ignorado y no rastreado; `.env.example` presente | Conservar evidencia sin secretos en informe |
| Serializers y validación | 15 | Serializer existente validado con pruebas de campos vacíos, tipos, rangos, categorías y reglas cruzadas; errores 400 | Capturas y explicación en informe |
| API REST | 25 | Listado, detalle, POST, PUT, PATCH y DELETE implementados y probados contra PostgreSQL de pruebas | Capturas de consumo HTTP exigidas por sección 6 |
| Autenticación y seguridad | 15 | Obtener/renovar JWT; 401 para falta de autenticación y 403 para falta de permiso; política documentada | Evidencias con tokens ocultos |
| Pruebas y evidencias | 10 | 35 pruebas automatizadas aprobadas y colección Postman preparada | Ejecutar colección en servidor, tomar capturas y explicar cada prueba. No se han generado esas capturas |
| Integración con el proyecto | 8 | Mismo modelo y base, cuatro apps existentes, CRUD HTML y contacto conservados; pruebas del sitio aprobadas; todas las migraciones aplicadas | Capturas de los cambios en Admin y aplicación junto a PostgreSQL |
| Documentación e IA | 7 | README actualizado con instalación, permisos, endpoints, ejemplos y pruebas; este registro describe el trabajo real | Informe PDF de evaluación 3 con capturas y reflexión propia del equipo; no encontrado en la carpeta revisada |
| Git y trabajo colaborativo | 5 | Rama `feature/api-rest`, remoto GitHub configurado e historial de varios autores | Cambios de esta intervención aún sin commit ni publicación. Confirmar que cada integrante tiene participación identificable |

Los puntos indican la ponderación de la pauta, no una nota asignada: falta evidencia de entrega para afirmar cumplimiento total.

## Verificaciones realizadas

- `python manage.py check`: sin problemas.
- Conexión real desde Django: PostgreSQL 18.6, base `parfums`.
- `python manage.py test catalogo contacto config --noinput`: 35 pruebas, OK, 28.044 segundos. Se creó y eliminó la base de pruebas separada de la aplicación.
- `python manage.py showmigrations --plan`: todas las migraciones marcadas como aplicadas.
- `python manage.py makemigrations --check --dry-run`: no hay cambios de modelos pendientes.
- `python -m pip check`: sin dependencias rotas.
- `.env` no aparece en `git ls-files` y `git check-ignore .env` confirma exclusión.
- Historial de la rama: autores Daniel-Soto-Zenteno, Mauro, nochi y sotomayormauro122-droid. El equipo debe confirmar las correspondencias con sus integrantes; no se suplantó participación ni se crearon commits en su nombre.

Estas verificaciones no constituyen una auditoría completa del historial para detectar secretos antiguos ni una revisión visual de todas las pantallas.

## Registro real de apoyo con IA

**Solicitud del usuario:** «C:\Users\diego\Downloads\ev1_backend-main trabaja ahi, con respecto a la rubrica, cumple con la solicitud numero 5 y verifica si cumple con lo demas».

**Problema detectado:** existían serializer, configuración DRF y rutas JWT, pero no estaban expuestas las operaciones REST del recurso.

**Propuesta aplicada:** reutilizar `PerfumeSerializer` en un `ModelViewSet`, agregar un router y exigir JWT en consultas y permiso de administrador en escrituras. La restricción administrativa mantiene la misma política de las modificaciones HTML. Reutilizar las validaciones ya existentes, sin inventar unicidad para nombres de perfumes.

**Verificación:** pruebas de respuestas, cambios persistidos en PostgreSQL, rechazo de escrituras anónimas y no autorizadas, validación parcial y conservación del funcionamiento HTML.

**Iteraciones anteriores observadas en este chat:** el arranque falló por `KeyError: SECRET_KEY`; se creó configuración local con clave aleatoria. La siguiente comprobación detectó que faltaba psycopg; se instalaron las dependencias y `manage.py check` pasó. En esta intervención la conexión PostgreSQL ya estaba configurada y se comprobó sin imprimir credenciales.

**Revisión pendiente del equipo:** explicar con sus propias palabras qué aceptaron o cambiarían, revisar el código y redactar su reflexión. No se inventaron decisiones, aprendizajes ni capturas atribuidos a los integrantes.

## Pasos pendientes para cerrar la evaluación

1. Ejecutar el servidor y la colección Postman con un usuario local administrador; sus pruebas verifican códigos HTTP y guardan tokens e identificador del perfume automáticamente.
2. Conservar capturas de las ocho pruebas de la sección 6: token, GET sin token, GET autorizado, POST, PUT/PATCH, DELETE, datos inválidos y POST sin token. La política de GET sin token es 401. Verificar también 403 con un usuario sin `is_staff`.
3. Documentar cambios visibles en aplicación/Admin/PostgreSQL usando un registro de demostración; la colección elimina su propio registro al finalizar.
4. Completar el informe PDF de evaluación 3 con explicación técnica, evidencias y reflexión personal del equipo.
5. Revisar los cambios y realizar commits identificables; actualizar GitHub. Nada de esta intervención fue publicado automáticamente.
