# T.P.I-de-programacion-
# Gestión de Datos de Países en Python

**Trabajo Práctico Integrador — Programación 1**

# Descripción

Aplicación de consola escrita en Python 3 que permite gestionar un conjunto de países
(nombre, población, superficie y continente). Los datos se leen desde un archivo CSV y se
guardan en memoria como una **lista de diccionarios**. Desde un menú interactivo se pueden
agregar y actualizar países, buscarlos, filtrarlos, ordenarlos y obtener estadísticas.

## Estructura del proyecto

```
.
├── main.py       # Programa principal con todas las funciones
├── paises.csv    # Dataset base (24 países)
└── README.md     # Este archivo
```

## Estructura de datos utilizada

Cada país es un **diccionario**:

```python
{"nombre": "Argentina", "poblacion": 45376763, "superficie": 2780400, "continente": "América"}
```

Y todos los países se guardan juntos en una **lista**:

```python
paises = [ {...}, {...}, {...} ]
```

## Requisitos

- Python 3.x (no necesita instalar librerías externas, solo usa el módulo `csv` de la librería estándar)

## Cómo ejecutarlo

```bash
python main.py
```

Al iniciar, el programa carga automáticamente `paises.csv`. Al salir con la opción `0`
(o con la opción `8`) los cambios se guardan de vuelta en el CSV.

## Menú de opciones

| Opción | Función |
|---|---|
| 1 | Agregar un país (no permite campos vacíos ni nombres duplicados) |
| 2 | Actualizar población y superficie de un país existente |
| 3 | Buscar país por nombre (coincidencia parcial) |
| 4 | Filtrar por continente, rango de población o rango de superficie |
| 5 | Ordenar por nombre, población o superficie (ascendente o descendente) |
| 6 | Mostrar estadísticas |
| 7 | Listar todos los países |
| 8 | Guardar los cambios en el CSV |
| 0 | Salir (guarda antes de cerrar) |

## Ejemplos de entrada / salida

### Buscar un país (opción 3)

```
Ingrese el nombre o parte del nombre: arg

NOMBRE                  POBLACION    SUPERFICIE  CONTINENTE
-----------------------------------------------------------------
Argentina                45376763       2780400  América
-----------------------------------------------------------------
Total: 1 pais/es
```

### Filtrar por continente (opción 4 → 1)

```
Continente a buscar: Oceanía

NOMBRE                  POBLACION    SUPERFICIE  CONTINENTE
-----------------------------------------------------------------
Australia                25687041       7692024  Oceanía
Nueva Zelanda             5084300        268021  Oceanía
-----------------------------------------------------------------
Total: 2 pais/es
```

### Estadísticas (opción 6)

```
--- ESTADISTICAS ---
Pais con MAYOR poblacion: China - 1412000000 habitantes
Pais con MENOR poblacion: Nueva Zelanda - 5084300 habitantes
Promedio de poblacion: 197711102.04 habitantes
Promedio de superficie: 2631660.21 km2

Cantidad de paises por continente:
 - América: 7
 - Asia: 5
 - Europa: 6
 - África: 4
 - Oceanía: 2
```

### Validación de errores

```
Poblacion: cuarenta
Debe ingresar un numero entero valido.
Poblacion: -5
El numero no puede ser negativo.
Poblacion: 45376763
```

## Validaciones implementadas

- Si el archivo CSV no existe, el programa avisa y arranca con la lista vacía en lugar de cortarse.
- Las filas del CSV con formato inválido (texto donde debería haber números) o con campos
  vacíos se informan y se ignoran, sin detener la carga del resto.
- No se permiten campos vacíos al cargar un país nuevo.
- No se permite cargar dos veces el mismo país.
- Población y superficie solo aceptan números enteros no negativos.
- En los filtros por rango, si el mínimo es mayor que el máximo los valores se intercambian
  automáticamente.
- Búsquedas y filtros sin resultados muestran un mensaje claro en lugar de una tabla vacía.
- Las opciones de menú inválidas muestran un mensaje de error y vuelven a pedir la opción.

## Conceptos de Programación 1 aplicados

- **Listas**: la colección completa de países y las listas de resultados de cada filtro.
- **Diccionarios**: cada país, y el conteo de países por continente.
- **Funciones**: el programa está modularizado, cada función cumple una sola responsabilidad.
- **Condicionales**: validaciones, selección de opciones del menú y comparaciones de los filtros.
- **Repetitivas**: `while` para el ciclo del menú y para revalidar entradas, `for` para recorrer la lista.
- **Ordenamientos**: implementación del método burbuja en la función `ordenar_paises()`.
- **Estadísticas**: máximo, mínimo, promedios y conteo por categoría.
- **Archivos CSV**: lectura con `csv.DictReader` y escritura con `csv.DictWriter`.

## Enlaces

- Documentación en PDF: *(agregar enlace o subir el PDF a la raíz del repositorio)*
- Video demostrativo: *(agregar enlace público de 10–15 min)*

## Integrantes y participación

| Integrante | Legajo | Tareas realizadas |
|---|---|---|
| *(Nombre y apellido)* | *(legajo)* | *(ej. carga y lectura del CSV, filtros, validaciones)* |
| *(Nombre y apellido)* | *(legajo)* | *(ej. ordenamientos, estadísticas, documentación)* |
