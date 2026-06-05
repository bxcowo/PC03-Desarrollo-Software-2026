# Guía Integral de Pruebas API - Voz del Ciudadano

Esta guía presenta los 7 pasos críticos para validar el sistema de forma secuencial y exitosa. Se detallan los datos de las llamadas y pruebas del proyecto con POSTMAN para su evaluación.

---

## 1. Registro de Ciudadano
Creación de la cuenta inicial para el ciudadano de prueba. Es fundamental para iniciar el flujo.
```bash
curl --location 'http://localhost:8000/auth/registro' \
--header 'Content-Type: application/json' \
--data '{
    "dni": "77777777",
    "nombre": "Usuario de Prueba",
    "email": "a.flores.a@gmail.com",
    "password": "password123"
}'
```
**Evidencia en Postman:**
![Evidencia de Registro](images/test1.png)

---

## 2. Inicio de Sesión (Autenticación)
Valida las credenciales y devuelve el token JWT real necesario para las operaciones protegidas.
```bash
curl --location 'http://localhost:8000/auth/login' \
--header 'Content-Type: application/json' \
--data '{
    "email": "a.flores.a@gmail.com",
    "password": "password123"
}'
```
**Evidencia en Postman:**
![Evidencia de Login](images/test2.png)

---

## 3. Crear Iniciativa Legislativa
Registra la iniciativa en la base de datos (Iniciativa ID: 1). Establece la propiedad necesaria para la gestión documental.
```bash
curl --location 'http://localhost:8000/iniciativas/' \
--header 'Authorization: Bearer eyJjaXVkYWRhbm9faWQiOiIxIiwiZW1haWwiOiJhLmZsb3Jlcy5hQGdtYWlsLmNvbSIsImlhdCI6IjIwMjYtMDYtMDVUMTk6MTY6MDUuNDQwNzY0KzAwOjAwIn0.e3d362fd6e0b5e80cace7278edf3ee84fc4850a79a0f1500175bb68fb63ea7c6' \
--header 'Content-Type: application/json' \
--data '{
    "titulo": "Ley de Fomento al Desarrollo Digital",
    "descripcion": "Propuesta para modernizar la infraestructura tecnológica nacional.",
    "dias_limite": 90
}'
```
**Resultado en Postman:**
![Evidencia de la iniciativa legislativa](images/test3.png) 

---

## 4. Registro de Firma Digital (HU-01)
Apoyo ciudadano a la iniciativa creada. Valida el DNI (Facade), bloquea duplicados (Proxy) y aplica lógica de validación (Decorator).
```bash
curl --location 'http://localhost:8000/firmas/' \
--header 'Authorization: Bearer eyJjaXVkYWRhbm9faWQiOiIxIiwiZW1haWwiOiJhLmZsb3Jlcy5hQGdtYWlsLmNvbSIsImlhdCI6IjIwMjYtMDYtMDVUMTk6MTY6MDUuNDQwNzY0KzAwOjAwIn0.e3d362fd6e0b5e80cace7278edf3ee84fc4850a79a0f1500175bb68fb63ea7c6' \
--header 'Content-Type: application/json' \
--data '{ "iniciativa_id": 1 }'
```
**Resultado en Postman:**
![Evidencia de la firma digital](images/test4.png) 

---

## 5. Inicializar Propuesta Normativa (HU-02 - Inicio)
Crea el objeto raíz documental para la iniciativa. Es un paso obligatorio antes de añadir contenido jerárquico.
```bash
curl --location 'http://localhost:8000/propuestas/' \
--header 'Authorization: Bearer eyJjaXVkYWRhbm9faWQiOiIxIiwiZW1haWwiOiJhLmZsb3Jlcy5hQGdtYWlsLmNvbSIsImlhdCI6IjIwMjYtMDYtMDVUMTk6MTY6MDUuNDQwNzY0KzAwOjAwIn0.e3d362fd6e0b5e80cace7278edf3ee84fc4850a79a0f1500175bb68fb63ea7c6' \
--header 'Content-Type: application/json' \
--data '{
    "iniciativa_id": 1,
    "titulo": "Estructura Documental: Ley Digital"
}'
```
**Resultado en Postman:**
![Evidencia de la propuesta normativa](images/test5.png) 

---

## 6. Construcción Jerárquica - Composite (HU-02)
Construye la propuesta añadiendo una sección y un artículo. Valida el patrón Composite al tratar hojas y compuestos uniformemente.
```bash
# 6.1 Agregar Sección
curl --location 'http://localhost:8000/propuestas/secciones' \
--header 'Authorization: Bearer eyJjaXVkYWRhbm9faWQiOiIxIiwiZW1haWwiOiJhLmZsb3Jlcy5hQGdtYWlsLmNvbSIsImlhdCI6IjIwMjYtMDYtMDVUMTk6MTY6MDUuNDQwNzY0KzAwOjAwIn0.e3d362fd6e0b5e80cace7278edf3ee84fc4850a79a0f1500175bb68fb63ea7c6' \
--header 'Content-Type: application/json' \
--data '{ "iniciativa_id": 1, "titulo_seccion": "Capítulo I" }'
```
**Resultado en Postman:**
![Evidencia de la agregacion de seccion](images/test6_1.png)

```bash
# 6.2 Agregar Artículo a la Sección "Capítulo I"
curl --location 'http://localhost:8000/propuestas/articulos' \
--header 'Authorization: Bearer eyJjaXVkYWRhbm9faWQiOiIxIiwiZW1haWwiOiJhLmZsb3Jlcy5hQGdtYWlsLmNvbSIsImlhdCI6IjIwMjYtMDYtMDVUMTk6MTY6MDUuNDQwNzY0KzAwOjAwIn0.e3d362fd6e0b5e80cace7278edf3ee84fc4850a79a0f1500175bb68fb63ea7c6' \
--header 'Content-Type: application/json' \
--data '{
    "iniciativa_id": 1,
    "titulo_seccion": "Capítulo I",
    "titulo_articulo": "Artículo 1",
    "contenido": "Texto legal detallado del artículo."
}'
```
**Resultado en Postman:**
![Evidencia de articulo a la seccion](images/test6_2.png)

---

## 7. Adjuntar Recurso Externo - Adapter (HU-02)
Valida el patrón Adapter mediante la subida de un archivo PDF, cuya información es extraída e integrada como anexo documental.
```bash
curl --location 'http://localhost:8000/propuestas/1/adjuntar' \
--header 'Authorization: Bearer eyJjaXVkYWRhbm9faWQiOiIxIiwiZW1haWwiOiJhLmZsb3Jlcy5hQGdtYWlsLmNvbSIsImlhdCI6IjIwMjYtMDYtMDVUMTk6MTY6MDUuNDQwNzY0KzAwOjAwIn0.e3d362fd6e0b5e80cace7278edf3ee84fc4850a79a0f1500175bb68fb63ea7c6' \
--form 'file=@"/ruta/a/tu/archivo.pdf"'
```
**Resultado en Postman:**
![Evidencia de recurso externo](images/test7.png)
