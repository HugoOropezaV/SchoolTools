import copy
import re

from flask import Flask, render_template, request
app = Flask(__name__, template_folder="../templates")
@app.get("/logica")
def logica():
    return render_template("logica.html")


def desarrolla_logica():
    frase_logica = request.form.get("frase_logica")
    frase_logica_corregida = corrige_proposiciones(frase_logica)
    if frase_logica_corregida == None:
        frase_logica_corregida = "no legible"
        return render_template("logica.html", frase_logica_corregida = frase_logica_corregida, frase_logica = frase_logica)

    lista_proposicion, lista_proposiciones = posibilidades_logicas(frase_logica_corregida)

    lista_proposicion_correcta = operadores_logicos(lista_proposicion)

    tabla_de_verdad_solucion = []
    tabla_de_verdad_no_polaca = []
    lista_proposicion_posible = lista_proposicion_correcta[:]
    lista_de_repeticiones = repeated_characters(lista_proposicion_correcta)
    for proposiciones in lista_proposiciones:
        i = 0
        lista_proposicion_correcta = lista_proposicion_posible[:]
        for termino in lista_proposicion_correcta:
            if termino == True or termino == False or len(termino) > 1:
                continue
            if 65 <= ord(termino) <= 90:
                for numero_repeticiones in range(lista_de_repeticiones[i + i + 1]):
                    lista_proposicion_correcta[lista_proposicion_correcta.index(termino)] = proposiciones[i]
                i += 1
        tabla_de_verdad_no_polaca.append(lista_proposicion_correcta)
        lista_proposicion_polaca = shuting_yard(lista_proposicion_correcta)
        tabla_de_verdad_solucion.append(lista_proposicion_polaca)

    columna_solucion = lista_proposiciones[:]


    for index in range(len(tabla_de_verdad_solucion)):
        tabla_de_verdad_solucion[index], columna_solucion[index] = desarrolla_metodo_polaco_inverso(tabla_de_verdad_solucion[index], tabla_de_verdad_no_polaca[index])

    clasificacion = clasifica_proposiciones_por_solucion(columna_solucion)
    tabla_de_verdad_solucion.insert(0, lista_proposicion_posible)
    for fila in lista_proposiciones:
        for index in range(len(fila)):
            if fila[index] == True:
                fila[index] = "V"
            elif fila[index] == False:
                fila[index] = "F"
    i = 0
    while i < len(lista_de_repeticiones):
        lista_de_repeticiones[i] = str(lista_de_repeticiones[i])
        if not 64 < ord(lista_de_repeticiones[i]) < 91:
            lista_de_repeticiones.pop(i)
            i -= 1
        i += 1


    lista_proposiciones.insert(0, lista_de_repeticiones)
    for posible in lista_proposiciones:
        posible.append(" ")
    for num_fila in range(len(tabla_de_verdad_solucion)):
        for index in range(len(lista_proposiciones[num_fila]) - 1, -1, -1):
            tabla_de_verdad_solucion[num_fila].insert(0, lista_proposiciones[num_fila][index])

    return render_template("logica.html", frase_logica = frase_logica, clasificacion = clasificacion, tabla_de_verdades = tabla_de_verdad_solucion, tabla_terminales = lista_proposiciones)

@app.post("/verifica_op_binarios")
def tablas_de_verdad_binarias(operando1, operando2, operador):
    if operador == "^":
        return (operando1 and operando2)

    elif operador == "v":
        return (operando1 or operando2)

    elif operador == "->":
        if operando1 == True and operando2 == False:
            return False
        else:
            return True

    elif operador == "<->":
        return(operando1 == operando2)
    else:
        return None

@app.post("/verifica_op_unarios")
def tablas_de_verdad_unarias(operando, operador):
    if operador == "~":
        return (not operando)
    else:
        return None

@app.post("/busca_repetidos")
def repeated_characters(lista_terminos):
    lista_repetidos = []#P,2,Q,1...
    for termino in lista_terminos:
        if len(termino) > 1:
            continue
        elif 65 <= ord(termino) <= 90:
            if termino in lista_repetidos:
                continue
            k = 0
            lista_repetidos.append(termino)
            for termino2 in lista_terminos:
                if termino == termino2:
                    k +=1
            lista_repetidos.append(k)
    return lista_repetidos

@app.post("/separador_logico")#operadores ^, v, ->, <->, ~
def operadores_logicos(lista_proposicion):
    index = 0
    lista_proposicion_correcta = []
    while index < len(lista_proposicion):
        termino = ""
        if lista_proposicion[index] == "<":
            while lista_proposicion[index] != ">":
                termino += lista_proposicion[index]
                index += 1
            termino += lista_proposicion[index]
        elif lista_proposicion[index] == "-":
            termino += lista_proposicion[index]
            index += 1
            termino += lista_proposicion[index]
        if termino != "":
            lista_proposicion_correcta.append(termino)
        else:
            lista_proposicion_correcta.append(lista_proposicion[index])
        index += 1
    return lista_proposicion_correcta

@app.post("/posibilidades")
def posibilidades_logicas(frase):
    mi_lista = [caracter for caracter in frase]

    terminales = 0
    for index in range(len(mi_lista)):
        if 97 <= ord(mi_lista[index]) <= 122 and ord(mi_lista[index]) != 118 :
            if chr(ord(mi_lista[index]) - 32) not in mi_lista:
                terminales += 1
            mi_lista[index] = chr(ord(mi_lista[index]) - 32)



    lista_proposiciones = []
    numero_combinaciones = 2 ** terminales
    valores = [True, False]

    for combo in range(numero_combinaciones):  # 0-7
        proposicion = []
        for divisor in range(terminales - 1, -1, -1):  # 0-2

            if (combo // (2 ** divisor)) % 2 == 0:
                proposicion.append(valores[0])
            else:
                proposicion.append(valores[1])

        lista_proposiciones.append(proposicion)

    return mi_lista, lista_proposiciones

@app.post("/algoritmo")
def shuting_yard(proposicion):
    lista_prioridad = ["(","<->", "->", "v", "^","~" ]
    queue = []
    pile = []
    index = 0
    for termino in proposicion:
        if termino == False or termino == True:

            queue.append(termino)

        elif termino == ")":

            while pile[len(pile) - 1][0] != "(":
                queue.append(pile.pop())
            pile.pop()
        else:
            tupla_parcial = (termino, index)

            index_termino_final = len(pile) - 1
            if len(pile) == 0:
                pile.append(tupla_parcial)
            elif lista_prioridad.index(termino) < lista_prioridad.index(pile[index_termino_final][0]) and lista_prioridad.index(termino) != 0:
                queue.append(pile.pop())
                pile.append(tupla_parcial)
            elif lista_prioridad.index(termino) != 0:
                pile.append(tupla_parcial)
            else:
                pile.append(termino)
        index += 1

    while pile != []:
        queue.append(pile.pop())

    return queue

@app.post("/polaco_inverso")
def desarrolla_metodo_polaco_inverso(cola, lista_no_polaca):

    index = 0
    while index < len(cola):
        if cola[index] != True and cola[index] != False :
            if cola[index][0] == "~":
                operando1 = cola.pop(index - 1)
                operador, pocision_original = cola.pop(index - 1)
                cola.insert(index - 1, tablas_de_verdad_unarias(operando1, operador))
                lista_no_polaca[pocision_original] = tablas_de_verdad_unarias(operando1, operador)
                index -= 1
                continue
            else:
                operando1 = cola.pop(index - 2)
                operando2 = cola.pop(index - 2)
                operador, pocision_original = cola.pop(index - 2)
                cola.insert(index - 2, tablas_de_verdad_binarias(operando1, operando2, operador))
                lista_no_polaca[pocision_original] = tablas_de_verdad_binarias(operando1,operando2, operador)
                index -= 2
                continue

        index += 1
    for index in range(len(lista_no_polaca)):
        if lista_no_polaca[index] == True:
            lista_no_polaca[index] = "V"
        elif lista_no_polaca[index] == False:
            lista_no_polaca[index] = "F"

    return lista_no_polaca, cola

@app.post("/clasificador")
def clasifica_proposiciones_por_solucion(soluciones_finales):
    filas_verdaderas = ""
    soluciones_verdaderas = [0,[]]
    for index in range(len(soluciones_finales)):
        if soluciones_finales[index][0] == True:
            soluciones_verdaderas[0] += 1
            soluciones_verdaderas[1].append(index + 1)

    for index in range(1, len(soluciones_verdaderas[1])):
        filas_verdaderas += (", " + str(soluciones_verdaderas[1][index]))

    if soluciones_verdaderas[0] == len(soluciones_finales):
        clasificacion = ("una tautología, y es satisfactible en todas las filas")
    elif 2 > soluciones_verdaderas[0] > 0:
        clasificacion = ("satisfactible en la fila: " + str(soluciones_verdaderas[1][0]) + filas_verdaderas)

    elif soluciones_verdaderas[0] > 0:
        clasificacion = ("satisfactible en las filas: " + str(soluciones_verdaderas[1][0]) + filas_verdaderas)
    elif soluciones_verdaderas[0] == 0:
        clasificacion = ("una contradicción, e insatisfactible en todas las filas")


    return clasificacion


@app.post("/borra_espacios_en_litas")
def elimina_espacios(lista):
    lista_a_entregar = []
    for elemento in lista:
        if elemento != " ":
            lista_a_entregar.append(elemento)
    return lista_a_entregar

@app.post("/corregidor")
def corrige_proposiciones(frase):
    frase = elimina_espacios(frase)
    frase.append(")")
    frase.insert(0, "(")

    lista_permitida1 = [x for x in range(97, 123)]  # minusculas
    lista_permitida2 = [x for x in range(65, 91)]  # mayusculas
    lista_permitida3 = [40, 41, 126, 45, 60, 62, 94, 118] #operadores/simbolos
    lista_permitida1.remove(118)
    lista_especial = [40, 41]

    parantesis_a = 0
    parantesis_c = 0

    for caracter in frase:
        if ord(caracter) in lista_permitida2:
            frase[frase.index(caracter)] = chr(ord(caracter) + 32)

    k = 0
    if len(frase) < 3:
        for x in range(len(frase)):
            if frase[x] != chr(126):
                if ord(frase[x]) not in lista_permitida1:
                    return None

                else:
                    k += 1
                    continue

        if 1 != k:
            return None
    else:
        final = frase[len(frase) - 1]
        if ord(final) != 41 or ord(frase[0]) != 40:
            if ord(final) in lista_permitida3 or (ord(frase[0]) in lista_permitida3 and ord(frase[0]) != 126):
                return None

    index = 0
    for caracter in frase:
        if ord(caracter) not in lista_permitida1 and ord(caracter) not in lista_permitida3:
            return None
        else:
            if caracter == "(" or caracter == "~":
                if ord(frase[index + 1]) not in lista_permitida1 and frase[index + 1] != "~" and frase[index + 1] != "(":
                    return None
                elif caracter == "(":
                    parantesis_a += 1
            elif caracter == ")":
                parantesis_c += 1
            elif caracter == "<":
                i = index
                signo_esperado = ""
                while i <= index + 2:
                    signo_esperado += frase[i]
                    i += 1
                if signo_esperado != "<->":
                    return None

                else:
                    index += 1
                    continue

            elif caracter == "-":
                if frase[index + 1] == ">":
                    index += 1
                    continue

                else:
                    return None
            elif caracter == ">":
                if frase[index - 1] != "-":
                    return None
            elif 0 < index < (len(frase) - 1):
                if ord(caracter) in lista_permitida1 and (ord(frase[index + 1]) in lista_permitida3 and ord(frase[index - 1]) in lista_permitida3):
                    index += 1
                    continue
                elif ord(caracter) in lista_permitida3 and (ord(frase[index + 1]) in lista_especial or ord(frase[index + 1]) in lista_permitida1 or ord(frase[index + 1]) == 126) and (ord(frase[frase.index(caracter) - 1]) in lista_especial or ord(frase[frase.index(caracter) - 1]) in lista_permitida1):
                    index += 1
                    continue
                else:
                    return None
        index += 1
    if parantesis_a != parantesis_c:
        return None
    frase.remove("(")
    frase.pop(len(frase) - 1)
    return frase
