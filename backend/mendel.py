
from flask import Flask, render_template, request
app = Flask(__name__, template_folder="../templates")

@app.post("/combinador")
def combinador(lista, cantidad_alelos):
    lista_combinaciones = []
    matriz_alelos = []

    numero_combinaciones = 2 ** cantidad_alelos
    for i in range(cantidad_alelos):
        alelos = []
        for j in range(2):
            alelito = str(lista.pop(0))
            alelos.append(alelito)
        matriz_alelos.append(alelos)

    for combo in range(numero_combinaciones): #0-3
        combinacion = ""
        for divisor in range(cantidad_alelos): #0-1

            if (combo // (2**divisor)) % 2 == 0:
                combinacion += matriz_alelos[divisor][0]
            else:
                combinacion += matriz_alelos[divisor][1]

        lista_combinaciones.append(combinacion)
    return lista_combinaciones

@app.post("/ordenador")
def ordenar(palabra):
    mi_palabra = ""
    palabra = list(palabra)
    palabra.sort(key = mi_llave)

    for letra in palabra:
       mi_palabra += letra

    return mi_palabra

@app.post("/mi_llave")
def mi_llave(caracter):
    numero = ord(caracter)
    if caracter > "Z":
        numero -= 31.5

    return numero

@app.get("/mendel")
def leyes_mendel_inicial():
    return render_template("mendel.html")

def leyes_mendel():

    lado_tabla = int(request.form.get("cantidad_alelos"))

    gameto11 = []
    gameto22 = []
    tabla = []



    if request.form.getlist("alelo1[]") == []:
        return render_template("mendel.html", cantidad_alelos=lado_tabla, gameto11 = gameto11, gameto22 = gameto22)

    gameto1 = request.form.getlist("alelo1[]")

    gameto2 = request.form.getlist("alelo2[]")

    gameto11 = gameto1[:]
    gameto22 = gameto2[:]

    if request.form.get("alelo_buscado") == None or request.form.get("alelo_buscado") == "" :
        alelo_buscado = "999999999"
    else:
        alelo_buscado = request.form.get("alelo_buscado")

    lista_combinaciones1 = combinador(gameto1, lado_tabla)
    lista_combinaciones2 = combinador(gameto2, lado_tabla)

    for i in range((lado_tabla * 2) + 1):
        tabla.append([])
        for j in range((lado_tabla * 2) + 1):
            tabla[i].append(0)

    for fila in range((lado_tabla * 2) + 1):

        for columna in range((lado_tabla * 2) + 1):
            if columna == 0 and fila == 0:
                tabla[fila][columna] = "gametos"
            elif columna == 0:
                tabla[fila][columna] = lista_combinaciones2[fila - 1]
            elif fila == 0:
                tabla[fila][columna] = lista_combinaciones1[columna - 1]
            else:
                tabla[fila][columna] = "--"
    for fila in range(1, (lado_tabla * 2) + 1):
        for columna in range(1, (lado_tabla * 2) + 1):
            elemento = ordenar(tabla[0][columna] + tabla[fila][0])
            if alelo_buscado in elemento:
                elemento = '<span class="encontrado">' + elemento + "</span>"
            tabla[fila][columna] = elemento

    gameto11.append( "".join(gameto11))
    gameto22.append( "".join(gameto22))

    return render_template("mendel.html",gameto22 = gameto22, gameto11 = gameto11, cantidad_alelos = lado_tabla, matriz_alelos = tabla, gameto1 = gameto1, gameto2 = gameto2, mi_alelo = elemento, alelo_buscado = alelo_buscado)

