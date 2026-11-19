import csv  # leer y escribir archivos CSV
import os   # verificar la existencia del archivo

ARCHIVO_CSV = "paises.csv"

# 1 MANEJO DE ARCHIVOS CSV

def cargar_paises(ruta):
    """Lee el archivo CSV y devuelve una lista de diccionarios con los paises"""
    paises = [] # aqui se van guardando los paises validos

    # Primera validacion: si el archivo no existe avisamos y devolvemos la
    # lista vacia. Asi el usuario puede empezar a cargar paises a mano.
    if not os.path.exists(ruta):
        print("ERROR: no se encontro el archivo", ruta)
        return paises

    try:
        # encoding="utf-8" es necesario para leer correctamente los acentos, 
        # o caracteres especiales
        archivo = open(ruta, "r", encoding="utf-8")

        # DictReader lee la primera fila como encabezado y convierte cada fila
        # siguiente en un diccionario cuyas claves son esos encabezados.
        lector = csv.DictReader(archivo)

        # Contador de filas. Arranca en 1 porque la fila 1 es el encabezado,
        # de modo que los avisos de error indiquen el numero real de linea.
        numero_fila = 1
        for fila in lector:
            numero_fila = numero_fila + 1
            try:
                # Armamos el diccionario del pais convirtiendo los campos
                # numericos con int(). Si el CSV trae texto en esos campos,
                # int() lanza ValueError y lo captura el except de abajo.
                # strip() elimina los espacios sobrantes al principio y al final.
                pais = {
                    "nombre": fila["nombre"].strip(),
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": fila["continente"].strip()
                }

                # Segunda validacion: los campos de texto no pueden estar vacios.
                if pais["nombre"] == "" or pais["continente"] == "":
                    print("Aviso: fila", numero_fila, "tiene campos vacios. Se ignora.")
                else:
                    paises.append(pais)

            # ValueError: el campo numerico no era un numero.
            # TypeError: el campo venia como None (faltaba una columna).
            # KeyError: el encabezado del CSV no tiene el nombre esperado.
            except (ValueError, TypeError, KeyError):
                print("Aviso: fila", numero_fila, "tiene un formato invalido. Se ignora.")

        archivo.close()
        print("Se cargaron", len(paises), "paises correctamente.")

    # OSError cubre los errores del sistema de archivos (permisos, disco, etc.)
    except OSError:
        print("ERROR: no se pudo abrir el archivo", ruta)

    return paises

def guardar_paises(ruta, paises):
    """Escribe la lista de paises en el archivo CSV, sobreescribiendo el anterior"""
    try:
        archivo = open(ruta, "w", encoding="utf-8", newline="")

        # fieldnames define el orden de las columnas en el archivo de salida.
        campos = ["nombre", "poblacion", "superficie", "continente"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)

        escritor.writeheader()  # Escribe la fila de encabezado
        for pais in paises:
            escritor.writerow(pais)  # Escribe un pais por fila

        archivo.close()
        print("Datos guardados en", ruta)
    except OSError:
        print("ERROR: no se pudieron guardar los datos.")

# 2 VALIDACION DE ENTRADAS DEL USUARIO
def pedir_texto(mensaje):
    """Pide un texto por teclado y lo vuelve a pedir mientras quede vacio"""

    texto = input(mensaje).strip()
    # Ciclo de revalidacion: no avanza hasta que el usuario escriba algo.
    while texto == "":
        print("El campo no puede quedar vacio.")
        texto = input(mensaje).strip()
    return texto

def pedir_entero_positivo(mensaje):
    """Pide un numero entero no negativo y revalida hasta que sea correcto"""

    while True:  # Ciclo infinito del que solo se sale con un valor valido
        entrada = input(mensaje).strip()
        try:
            numero = int(entrada)  # Si no es un numero, salta a except
            if numero < 0:
                print("El numero no puede ser negativo.")
            else:
                return numero  # Valor valido: se devuelve y termina el ciclo
        except ValueError:
            print("Debe ingresar un numero entero valido.")

# 3: SALIDA POR PANTALLA Y BUSQUEDA INTERNA
def mostrar_paises(paises):
    """Muestra una lista de paises en formato de tabla alineada"""
    if len(paises) == 0:
        print("No hay paises para mostrar.")
        return

    print("")
    # ljust() alinea el texto a la izquierda y rjust() a la derecha,
    # rellenando con espacios para que las columnas queden parejas.
    print("NOMBRE".ljust(18), "POBLACION".rjust(14), "SUPERFICIE".rjust(13), " CONTINENTE")
    print("-" * 65)  # Linea separadora de 65 guiones

    for pais in paises:
        # Los numeros se convierten a str() porque rjust() solo opera sobre texto.
        print(pais["nombre"].ljust(18),
              str(pais["poblacion"]).rjust(14),
              str(pais["superficie"]).rjust(13),
              " " + pais["continente"])

    print("-" * 65)
    print("Total:", len(paises), "pais/es")
    print("")

def buscar_indice_por_nombre(paises, nombre):
    """Busca un pais por nombre exacto y devuelve su posicion en la lista.

    Se usa internamente para detectar duplicados al agregar y para ubicar
    el pais a modificar al actualizar. La comparacion se hace en minusculas
    con lower() para que "argentina" y "Argentina" se consideren iguales.
    """
    posicion = 0
    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            return posicion  # Encontrado: devuelve el indice y corta el ciclo
        posicion = posicion + 1
    return -1  # Recorrio toda la lista sin encontrarlo

# 4: ALTA Y MODIFICACION DE PAISES
def agregar_pais(paises):
    """Pide los datos de un pais nuevo y lo agrega a la lista"""

    print("")
    print("--- AGREGAR PAIS ---")

    nombre = pedir_texto("Nombre del pais: ")

    # Control de duplicados: si el nombre ya existe, se corta la operacion
    # antes de pedir el resto de los datos.
    if buscar_indice_por_nombre(paises, nombre) != -1:
        print("ERROR: el pais", nombre, "ya esta cargado.")
        return

    poblacion = pedir_entero_positivo("Poblacion: ")
    superficie = pedir_entero_positivo("Superficie en km2: ")
    continente = pedir_texto("Continente: ")

    # Se arma el diccionario con las cuatro claves del dominio.
    pais_nuevo = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }

    paises.append(pais_nuevo)  # append() agrega el pais al final de la lista
    print("EXITO: el pais", nombre, "se agrego correctamente.")


def actualizar_pais(paises):
    """Actualiza la poblacion y la superficie de un pais ya cargado"""
    print("")
    print("--- ACTUALIZAR PAIS ---")
    # primera validacion
    if len(paises) == 0:
        print("No hay paises cargados.")
        return

    nombre = pedir_texto("Nombre del pais a actualizar: ")
    posicion = buscar_indice_por_nombre(paises, nombre)

    # Segunda validacion: el pais debe existir.
    if posicion == -1:
        print("ERROR: no se encontro el pais", nombre)
        return

    # Se muestran los datos actuales para que el usuario confirme visualmente
    # que es el pais correcto. Se pasa una lista de un solo elemento porque
    # mostrar_paises() espera una lista.
    print("Datos actuales:")
    mostrar_paises([paises[posicion]])

    nueva_poblacion = pedir_entero_positivo("Nueva poblacion: ")
    nueva_superficie = pedir_entero_positivo("Nueva superficie en km2: ")

    # Se modifican solo las dos claves pedidas por la consigna.
    # El nombre y el continente quedan intactos.
    paises[posicion]["poblacion"] = nueva_poblacion
    paises[posicion]["superficie"] = nueva_superficie

    print("EXITO: los datos de", paises[posicion]["nombre"], "se actualizaron.")

# 5: BUSQUEDAS Y FILTROS
def buscar_pais(paises):
    """Busca paises cuyo nombre contenga el texto ingresado"""
    print("")
    print("--- BUSCAR PAIS ---")
    texto = pedir_texto("Ingrese el nombre o parte del nombre: ")

    encontrados = []  # Lista de resultados
    for pais in paises:
        # El operador "in" sobre cadenas verifica que el texto este contenido
        # en el nombre. lower() en ambos lados hace la busqueda insensible
        # a mayusculas: "arg" encuentra "Argentina".
        if texto.lower() in pais["nombre"].lower():
            encontrados.append(pais)

    # Validacion de busqueda sin resultados: mensaje claro en lugar de
    # una tabla vacia.
    if len(encontrados) == 0:
        print("No se encontraron paises que coincidan con:", texto)
    else:
        mostrar_paises(encontrados)

def filtrar_por_continente(paises):
    """Filtra los paises que pertenecen a un continente determinado"""
    continente = pedir_texto("Continente a buscar: ")

    encontrados = []
    for pais in paises:
        if pais["continente"].lower() == continente.lower():
            encontrados.append(pais)

    if len(encontrados) == 0:
        print("No hay paises cargados del continente:", continente)
    else:
        mostrar_paises(encontrados)

def filtrar_por_rango(paises, campo):
    """Filtra los paises cuyo campo numerico este entre un minimo y un maximo"""
    minimo = pedir_entero_positivo("Valor minimo: ")
    maximo = pedir_entero_positivo("Valor maximo: ")

    # Validacion de filtro invalido: si el usuario invierte los valores,
    # en lugar de devolver una lista vacia se intercambian usando una
    # variable auxiliar y se avisa de la correccion.
    if minimo > maximo:
        print("Aviso: el minimo era mayor que el maximo, se intercambiaron los valores.")
        auxiliar = minimo
        minimo = maximo
        maximo = auxiliar

    encontrados = []
    for pais in paises:
        # Condicion compuesta con "and": el valor debe estar dentro del rango,
        # incluyendo los extremos.
        if pais[campo] >= minimo and pais[campo] <= maximo:
            encontrados.append(pais)

    if len(encontrados) == 0:
        print("Ningun pais entra en ese rango.")
    else:
        mostrar_paises(encontrados)

def menu_filtros(paises):
    """Muestra el submenu de filtros y deriva a la funcion correspondiente"""
    print("")
    print("--- FILTRAR PAISES ---")
    print("1. Por continente")
    print("2. Por rango de poblacion")
    print("3. Por rango de superficie")
    print("0. Volver")

    opcion = input("Opcion: ").strip()

    # Estructura condicional multiple: cada opcion llama a una funcion distinta.
    # Las opciones 2 y 3 reutilizan filtrar_por_rango() cambiando solo el campo.
    if opcion == "1":
        filtrar_por_continente(paises)
    elif opcion == "2":
        filtrar_por_rango(paises, "poblacion")
    elif opcion == "3":
        filtrar_por_rango(paises, "superficie")
    elif opcion == "0":
        print("Volviendo al menu principal...")
    else:
        # Validacion de opcion invalida: mensaje de error y se vuelve al menu.
        print("ERROR: opcion invalida.")

# 6: ORDENAMIENTO
def ordenar_paises(paises, campo, descendente):
    """Ordena una copia de la lista"""
    # copy() crea una lista nueva para no alterar el orden de la lista original,
    # que es la que se guarda en el CSV.
    lista = paises.copy()
    cantidad = len(lista)

    # Ciclo externo: controla la cantidad de pasadas. Con n elementos
    # alcanzan n-1 pasadas para dejar todo ordenado.
    for i in range(cantidad - 1):
        # Ciclo interno: recorre los pares contiguos. Se resta "i" porque
        # los ultimos "i" elementos ya quedaron ordenados en las pasadas
        # anteriores y no hace falta volver a compararlos.
        for j in range(cantidad - 1 - i):
            valor_actual = lista[j][campo]
            valor_siguiente = lista[j + 1][campo]

            # Si se ordena por nombre, se comparan los textos en minusculas
            # para que las mayusculas no alteren el orden alfabetico.
            if campo == "nombre":
                valor_actual = valor_actual.lower()
                valor_siguiente = valor_siguiente.lower()

            # La direccion del orden se decide invirtiendo la comparacion.
            if descendente:
                hay_que_intercambiar = valor_actual < valor_siguiente
            else:
                hay_que_intercambiar = valor_actual > valor_siguiente

            # Intercambio clasico con variable auxiliar.
            if hay_que_intercambiar:
                auxiliar = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = auxiliar

    return lista


def menu_ordenar(paises):
    """Muestra el submenu de ordenamiento, pide la direccion y muestra el resultado"""
    print("")
    print("--- ORDENAR PAISES ---")
    print("1. Por nombre")
    print("2. Por poblacion")
    print("3. Por superficie")
    print("0. Volver")

    opcion = input("Opcion: ").strip()

    # Salida temprana: si elige volver, no se pide nada mas.
    if opcion == "0":
        print("Volviendo al menu principal...")
        return

    # Se traduce la opcion del menu al nombre de la clave del diccionario.
    if opcion == "1":
        campo = "nombre"
    elif opcion == "2":
        campo = "poblacion"
    elif opcion == "3":
        campo = "superficie"
    else:
        print("ERROR: opcion invalida.")
        return

    # upper() permite aceptar tanto "a" como "A".
    orden = input("Orden (A = ascendente / D = descendente): ").strip().upper()
    if orden == "A":
        descendente = False
    elif orden == "D":
        descendente = True
    else:
        # Ante una entrada no reconocida se avisa y se usa un valor por
        # defecto, en lugar de cortar la operacion.
        print("Aviso: no se reconocio el orden, se usa ascendente por defecto.")
        descendente = False

    lista_ordenada = ordenar_paises(paises, campo, descendente)
    mostrar_paises(lista_ordenada)

# 7: ESTADISTICAS
def mostrar_estadisticas(paises):
    """Calcula y muestra los indicadores principales del dataset"""
    print("")
    print("--- ESTADISTICAS ---")

    # Validacion: sin datos no se puede calcular un promedio (division por cero).
    if len(paises) == 0:
        print("No hay paises cargados para calcular estadisticas.")
        return

    # Se toma el primer pais como referencia inicial del maximo y del minimo.
    # Asi la comparacion del ciclo siempre tiene con que comparar.
    pais_mayor = paises[0]
    pais_menor = paises[0]
    suma_poblacion = 0
    suma_superficie = 0

    # Un unico recorrido calcula las cuatro cosas a la vez: maximo, minimo
    # y las dos sumas acumuladas.
    for pais in paises:
        if pais["poblacion"] > pais_mayor["poblacion"]:
            pais_mayor = pais
        if pais["poblacion"] < pais_menor["poblacion"]:
            pais_menor = pais
        suma_poblacion = suma_poblacion + pais["poblacion"]
        suma_superficie = suma_superficie + pais["superficie"]

    # El promedio es la suma acumulada dividida por la cantidad de elementos.
    cantidad = len(paises)
    promedio_poblacion = suma_poblacion / cantidad
    promedio_superficie = suma_superficie / cantidad

    print("Pais con MAYOR poblacion:", pais_mayor["nombre"], "-", pais_mayor["poblacion"], "habitantes")
    print("Pais con MENOR poblacion:", pais_menor["nombre"], "-", pais_menor["poblacion"], "habitantes")
    # round(x, 2) recorta el promedio a dos decimales para que se lea mejor.
    print("Promedio de poblacion:", round(promedio_poblacion, 2), "habitantes")
    print("Promedio de superficie:", round(promedio_superficie, 2), "km2")

    # Conteo por categoria usando un DICCIONARIO como contador:
    # la clave es el continente y el valor la cantidad acumulada.
    conteo_continentes = {}
    for pais in paises:
        continente = pais["continente"]
        # Si el continente ya aparecio, se suma 1 al valor existente.
        # Si es la primera vez, se crea la clave con el valor 1.
        if continente in conteo_continentes:
            conteo_continentes[continente] = conteo_continentes[continente] + 1
        else:
            conteo_continentes[continente] = 1

    print("")
    print("Cantidad de paises por continente:")
    # Al recorrer un diccionario con "for" se obtienen sus claves.
    for continente in conteo_continentes:
        print(" -", continente + ":", conteo_continentes[continente])
    print("")

# 8: MENU PRINCIPAL Y PROGRAMA
def mostrar_menu():
    """Imprime en pantalla el menu principal de opciones."""
    print("")
    print("=" * 45)
    print("   GESTION DE PAISES - PROGRAMACION 1")
    print("=" * 45)
    print("1. Agregar un pais")
    print("2. Actualizar poblacion y superficie")
    print("3. Buscar pais por nombre")
    print("4. Filtrar paises")
    print("5. Ordenar paises")
    print("6. Mostrar estadisticas")
    print("7. Listar todos los paises")
    print("8. Guardar cambios en el CSV")
    print("0. Salir")
    print("=" * 45)


def main():
    """Funcion principal: carga los datos y ejecuta el ciclo del menu."""
    # Carga inicial del dataset al arrancar el programa.
    paises = cargar_paises(ARCHIVO_CSV)

    # La opcion arranca como texto vacio para que el ciclo se ejecute
    # al menos una vez (el usuario todavia no eligio nada).
    opcion = ""

    # Ciclo principal: se repite hasta que el usuario elija salir con "0".
    while opcion != "0":
        mostrar_menu()
        # Se lee la opcion como texto (no con int()) para que una letra
        # no rompa el programa: simplemente no coincide con ninguna opcion.
        opcion = input("Elija una opcion: ").strip()

        # Estructura condicional multiple que deriva a cada funcionalidad.
        if opcion == "1":
            agregar_pais(paises)
        elif opcion == "2":
            actualizar_pais(paises)
        elif opcion == "3":
            buscar_pais(paises)
        elif opcion == "4":
            menu_filtros(paises)
        elif opcion == "5":
            menu_ordenar(paises)
        elif opcion == "6":
            mostrar_estadisticas(paises)
        elif opcion == "7":
            mostrar_paises(paises)
        elif opcion == "8":
            guardar_paises(ARCHIVO_CSV, paises)
        elif opcion == "0":
            # Antes de cerrar se persisten los cambios en el CSV para no
            # perder las altas y modificaciones hechas durante la sesion.
            guardar_paises(ARCHIVO_CSV, paises)
            print("Programa finalizado. Hasta luego!")
        else:
            print("ERROR: opcion invalida. Elija un numero del menu.")

if __name__ == "__main__":
    main()
