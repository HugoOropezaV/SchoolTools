import copy
import re

from flask import Flask, render_template, request
app = Flask(__name__, template_folder="../templates")

class Termino_bonito:
    def __init__(self, coheficiente, especie):
        self.coheficiente = coheficiente
        self.especie = especie
    pass

@app.get("/analitica")
def analitica():
    return render_template("analitica.html")

@app.post("/borra_espacios_en_listas")
def elimina_espacios(lista):
    lista_a_entregar = []
    for elemento in lista:
        if elemento != " ":
            lista_a_entregar.append(elemento)
    return lista_a_entregar

@app.post("/llena_coheficientes_vacios")
def corrige_coheficientes_vacios(lista_de_coheficientes):  # para esta funcion, usar "©" como simbolo de coheficiente vacio (ascii 184)
    numero_slashes = 0
    for posible_coheficiente in lista_de_coheficientes:
        for caracter in posible_coheficiente:
            if caracter == "/":
                numero_slashes += 1
        if numero_slashes > 1:
            return True
        else:
            numero_slashes = 0
    for indice in range(len(lista_de_coheficientes)):

        if lista_de_coheficientes[indice] == "©":
            lista_de_coheficientes[indice] = 1
        else:
            for index in range(len(lista_de_coheficientes[indice])) :
                if lista_de_coheficientes[indice][index] == "/":
                    numerador, denominador = simplificador_de_fracciones(lista_de_coheficientes[indice][0:index], lista_de_coheficientes[indice][index + 1:])
                    lista_de_coheficientes[indice] = numerador / denominador
                    break
        lista_de_coheficientes[indice] = float(lista_de_coheficientes[indice])
    return lista_de_coheficientes

@app.post("/simplificador")
def simplificador_de_fracciones(numerador, denominador):

   numerador = float(numerador)
   denominador = float(denominador)
   divisor = 2

   if numerador == denominador:
      return 1, 1
   elif numerador > denominador:
      div_max = numerador
   else:
      div_max = denominador

   lista_enteros = [x for x in range(1, int(div_max))]
   while divisor <= div_max:
      if numerador / divisor in lista_enteros and denominador / divisor in lista_enteros:
         numerador /= divisor
         denominador /= divisor
      else:
         divisor += 1
   if denominador < 0.0 and numerador > 0.0:
      numerador *= -1
      denominador *= -1
   return numerador, denominador

@app.post("/separa_terminos")
def separa_terminos_algebraicos(mi_ecuacion):
   lista_de_terminos = []
   indice = 1
   while (indice < len(mi_ecuacion)):  # separa los terminos
      if mi_ecuacion[indice - 1] == "+" or mi_ecuacion[indice - 1] == "-":
         termino = [mi_ecuacion[indice - 1]]

         while (mi_ecuacion[indice] != "+" and mi_ecuacion[indice] != "-"):
            termino.append(mi_ecuacion[indice])
            indice += 1
            if indice == len(mi_ecuacion):
               break

         lista_de_terminos.append(termino)

      indice += 1
   return lista_de_terminos

@app.post("/llena_coheficientes")
def llena_coheficientes_str(mi_ecuacion):
   lista_de_coheficientes = []
   coheficiente_temporal = ""
   mi_ecuacion.append(" ")
   posicion = 0

   for elemento in mi_ecuacion:
       if elemento == "+" or elemento == "-":
           lista_de_coheficientes.append("©")

   for indice in range(1, len(mi_ecuacion) - 1):    # concatena coheficientes (str)

       if 48 <= ord(mi_ecuacion[indice]) <= 57 or ord(mi_ecuacion[indice]) == 184 or ord(mi_ecuacion[indice]) == 46  or ord(mi_ecuacion[indice]) == 47:
           if mi_ecuacion[indice - 1] != "^":
              if 48 <= ord(mi_ecuacion[indice + 1]) <= 57 or mi_ecuacion[indice + 1] == "x" or mi_ecuacion[indice + 1] == "y" \
                 or mi_ecuacion[indice + 1] == " " or mi_ecuacion[indice + 1] == "+" \
                    or mi_ecuacion[indice + 1] == "-" or mi_ecuacion[indice + 1] == "." or ord(mi_ecuacion[indice + 1]) == 47:

                 if ord(mi_ecuacion[indice]) == 184:
                    coheficiente_temporal = "-1"
                    lista_de_coheficientes[posicion] = coheficiente_temporal

                 else:
                    coheficiente_temporal += mi_ecuacion[indice]
                    lista_de_coheficientes[posicion] = coheficiente_temporal



       if mi_ecuacion[indice] == "x" or mi_ecuacion[indice] == "y":
           posicion += 1
           coheficiente_temporal = ""

       elif mi_ecuacion[indice] != "₡":

           if mi_ecuacion[indice + 1] == "+" or mi_ecuacion[indice + 1] == "-":

              if mi_ecuacion[indice - 1] != "^":
                 posicion += 1
                 coheficiente_temporal = ""


   return lista_de_coheficientes

@app.post("/delata_errores")
def busca_errores(mi_ecuacion):



    mi_ecuacion.append(" ")
    lista_prohibida1 = [x for x in range(95, 120)] #minusculas
    lista_prohibida2 = [x for x in range(58, 94)]#mayusculas
    lista_prohibida3 = [x for x in range(33, 43)]

    lista_prohibida1.append(44)
    #lista_prohibida1.append(46)
    #lista_prohibida1.append(47)
    for caracter in mi_ecuacion:
       if 32 <= ord(caracter) <= 121:
            if ord(caracter)  not in lista_prohibida1 and ord(caracter) not in lista_prohibida2 and ord(caracter) not in lista_prohibida3:
                variable_de_adorno = 0
            else:
                return True
       else:
            return True
    lista_numeros = [x for x in range(48, 58)]
    for indice in range(1, len(mi_ecuacion)):
        if mi_ecuacion[indice - 1] == "^":
            if 51 <= ord(mi_ecuacion[indice]) <= 57:
                return True
            elif 48 <= ord(mi_ecuacion[indice]) <= 50:
                if 48 <= ord(mi_ecuacion[indice + 1]) <= 57:
                    return True
    for indice in range(len(mi_ecuacion) - 1):
        if mi_ecuacion[indice] == "+" or mi_ecuacion[indice] == "-" or mi_ecuacion[indice] == "^" or mi_ecuacion[indice] == "/":
            if mi_ecuacion[indice + 1] == "+" or mi_ecuacion[indice + 1] == "-" or mi_ecuacion[indice + 1] == "^" or mi_ecuacion[indice + 1] == "/":
                return True
        if mi_ecuacion[indice + 1] == "^":
            if ord(mi_ecuacion[indice]) in lista_numeros:
                return True

    for indice in range(1, len(mi_ecuacion) - 1):
        if mi_ecuacion[indice] == "/":
            if ord(mi_ecuacion[indice - 1]) not in lista_numeros or ord(mi_ecuacion[indice + 1]) not in lista_numeros:
                return True

    for indice in range(len(mi_ecuacion) - 1):
        if mi_ecuacion[indice] == "x" or mi_ecuacion[indice] == "y":
            if ord(mi_ecuacion[indice + 1]) in lista_numeros:
                return True
    for indice in range(len(mi_ecuacion) -2):
        if mi_ecuacion[indice] == "^":
            if mi_ecuacion[indice + 2] != "+":
                if mi_ecuacion[indice + 2] != "-":
                    if mi_ecuacion[indice + 2] != " ":
                        return True

    return False

@app.post("/reformulador")#x2 y2 xy  x  y  1
def rearmador_de_ecuaciones(A, B, C, D, E, F):

    ecuacion_reformulada = ""



    if A != 0:
        if A > 0:
            ecuacion_reformulada += "+" + str(A) + "x^2"
        else:
            ecuacion_reformulada += str(A) + "x^2"

    if B != 0:
        if B > 0:
            ecuacion_reformulada += "+" + str(B) + "y^2"
        else:
            ecuacion_reformulada += str(B) + "y^2"
    if C != 0:
        if C > 0:
            ecuacion_reformulada += "+" + str(C) + "xy"
        else:
            ecuacion_reformulada += str(C) + "xy"
    if D != 0:
        if D > 0:
            ecuacion_reformulada += "+" + str(D) + "x"
        else:
            ecuacion_reformulada += str(D) + "x"
    if E != 0:
        if E > 0:
            ecuacion_reformulada += "+" + str(E) + "y"
        else:
            ecuacion_reformulada += str(E) + "y"
    if F != 0:
        if F > 0:
            ecuacion_reformulada += "+" + str(F)
        else:
            ecuacion_reformulada += str(F)




    print(ecuacion_reformulada)
    return ecuacion_reformulada

@app.post("/mi_ecuacion_organizada")
def organizar_ecuacion_conica(ecuacion):
    mi_ecuacion = []
    termino = []
    for caracter in ecuacion:
        if caracter != " ":
            mi_ecuacion.append(caracter)
    if mi_ecuacion[0] != "-" and mi_ecuacion[0] != "+":
        mi_ecuacion.insert(0, "+")

    if busca_errores(mi_ecuacion) == True:
        return ecuacion, ecuacion
    elif busca_errores(mi_ecuacion) == 123:
        return 1,2

    for indice in range(1, len(mi_ecuacion)):
        if (mi_ecuacion[indice] == "y" ) and (mi_ecuacion[indice - 1] == "x"):
            mi_ecuacion[indice] = "₡"
        elif (mi_ecuacion[indice] == "x") and (mi_ecuacion[indice - 1] == "y"):
            mi_ecuacion[indice - 1] = "₡"




    lista_de_coheficientes = llena_coheficientes_str(mi_ecuacion)

    lista_de_coheficientes = corrige_coheficientes_vacios(lista_de_coheficientes)
    if lista_de_coheficientes == True:
        return 0, 0
    mi_ecuacion = elimina_espacios(mi_ecuacion)

    lista_de_terminos = separa_terminos_algebraicos(mi_ecuacion)


    ecuacion_publica = copy.deepcopy(lista_de_terminos)
    indice = 0
    for termino in lista_de_terminos: #elimina terminos innecesarios de mostrar
        if termino[1] == "0" and termino[2] == "0":
            del ecuacion_publica[indice]
        indice += 1
    for termino in ecuacion_publica:
        for caracter in range(1, len(termino)):
            if termino[caracter] == "₡":
                termino[caracter] = "y"
    for termino in lista_de_terminos:
        for caracter in range(1, len(termino)):
            if termino[caracter] == "₡":
                termino[caracter] = "y"

    repartidor = 0
    for termino in lista_de_terminos:   # arma coheficiente en los terminos
        termino.append(" ")
        indice = 0

        while (termino[indice] != "x" and termino[indice] != "y" and termino[indice] != " "):
            if termino[indice] == "+":
                coheficiente = 1
            if termino[indice] == "-":
                coheficiente = -1

            if termino[indice + 1] == "x" or termino[indice + 1] == "y" or termino[indice + 1] == " ":

                for posicion in range(indice, -1, -1):
                    del termino[posicion]
                termino.insert(0, (coheficiente * lista_de_coheficientes[repartidor]))
                repartidor += 1
                break

            indice += 1

        termino.remove(" ")

    lista_de_objetos = []
    for elemento in lista_de_terminos:
        mi_coheficiente = elemento.pop(0)
        aux = "".join(elemento)
        elemento.clear()
        elemento.append(aux)
        mi_especie = elemento.pop(0)
        termino = Termino_bonito(mi_coheficiente, mi_especie)

        lista_de_objetos.append(termino)
    return lista_de_objetos, ecuacion_publica

@app.post("/identificador")
def identificar_figura_conica(A, B):
    figura_conica = ""

    if A == B:
        figura_conica = "circunferencia"
    elif A == 0 or B == 0:
        figura_conica = "parabola"
    elif A * B > 0 and A != B:
        figura_conica = "elipse"
    elif A * B < 0:
        figura_conica = "hiperbola"

    return figura_conica

@app.post("/desarrollador1")
def desarrollar_circunferencia(A, B, D, E, F, H, K):

    if H != "" and K != "":
        h = H
        k = K
        if ((-1 * F) / A + (D / (2 * A)) ** 2 + (E / (2 * B)) ** 2) > 0:
            radio = ((-1 * F) / A + (D / (2 * A)) ** 2 + (E / (2 * B)) ** 2) ** (1/2)
        else:
            return None

    else:
        if D == 0:
            h = 0

        else:
            h = D / (-2 * A)
        if E == 0:
            k = 0

        else:
            k = E / (-2 * B)
        if ((-1 * F) / A + (D / (2 * A)) ** 2 + (E / (2 * B)) ** 2) > 0:
            radio = ((-1 * F) / A + (D / (2 * A)) ** 2 + (E / (2 * B)) ** 2) ** (1/2)
        else:
            return None

    return h,k,radio

@app.post("/desarrollador2")
def desarrollar_parabola(A, B, D, E, F, orintacion, H, K):

    if H != "" and K != "":
        return None
    else:
        if D == 0 and E == 0:
            return None

        elif orintacion == "vertical":

            D /= A
            E /= A
            F /= A
            A /= A
            if D == 0 :
                V_h = 0
                if F == 0:
                    V_k = 0
                else:
                    V_k = (-1 * F) / E
            else:
                V_h = D / (-2 * A)
                V_k = (F - ((D / 2) ** 2)) / (- E)
            F_h = V_h
            F_k = V_k - (E / 4)
            d_focal = E / (-4)
            L_recto = abs(d_focal) * 4

        else:

            D /= B
            E /= B
            F /= B
            B /= B
            if E == 0 :
                V_k = 0
                if F == 0:
                    V_h = 0
                else:
                    V_h = (-1 * F) / D
            else:
                V_k = E / (-2 * B)
                V_h = (F - ((E / 2) ** 2)) / (- D)
            F_k = V_k
            F_h = V_h - (D / 4)
            d_focal = D / (-4)
            L_recto = abs(d_focal) * 4

    return F_h, F_k, V_h, V_k, L_recto, d_focal

@app.post("/desarrollador3")
def desarrollar_elipse(A, B, D, E, F, orintacion, H, K):

    Centro_h = -1 * D / (2 * A)
    Centro_k = -1 * E / (2 * B)
    if D == 0 and E == 0 and F >= 0:
        return None

    elif orintacion == "vertical":
        a_mayor = 1 / (((B) /((-1 * F) + ((D ** 2) / (4 * A) ) + ((E ** 2) / (4 * B)))) ** (1 / 2))
        b_menor = 1 / (((A) / ((-1 * F) + ((D ** 2) / (4 * A)) + ((E ** 2) / (4 * B)))) ** (1 / 2))
        c_focal = ((a_mayor ** 2) - (b_menor ** 2)) ** (1/2)

        Vertice_h = Centro_h
        Vertice_k = Centro_k + a_mayor
        Vertice_prima_h = Centro_h
        Vertice_prima_k = Centro_k - a_mayor

        Vertice_sec_h = Centro_h + b_menor
        Vertice_sec_k = Centro_k
        Vertice_sec_prima_h = Centro_h - b_menor
        Vertice_sec_prima_k = Centro_k

        Foco_h = Centro_h
        Foco_k = Centro_k + c_focal
        Foco_prima_h = Centro_h
        Foco_prima_k = Centro_k - c_focal

        Lado_recto = (2 * (b_menor ** 2)) / a_mayor
        excentricidad = c_focal / a_mayor

    else:
        a_mayor = 1 / (((A) / ((-1 * F) + ((D ** 2) / (4 * A)) + ((E ** 2) / (4 * B)))) ** (1 / 2))
        b_menor = 1 / (((B) / ((-1 * F) + ((D ** 2) / (4 * A)) + ((E ** 2) / (4 * B)))) ** (1 / 2))
        c_focal = ((a_mayor ** 2) - (b_menor ** 2)) ** (1 / 2)

        Vertice_h = Centro_h + a_mayor
        Vertice_k = Centro_k
        Vertice_prima_h = Centro_h - a_mayor
        Vertice_prima_k = Centro_k

        Vertice_sec_h = Centro_h
        Vertice_sec_k = Centro_k + b_menor
        Vertice_sec_prima_h = Centro_h
        Vertice_sec_prima_k = Centro_k - b_menor

        Foco_h = Centro_h + c_focal
        Foco_k = Centro_k
        Foco_prima_h = Centro_h - c_focal
        Foco_prima_k = Centro_k

        Lado_recto = (2 * (b_menor ** 2)) / a_mayor
        excentricidad = c_focal / a_mayor





    return a_mayor, b_menor, c_focal,Centro_h, Centro_k, Vertice_h, Vertice_k, Vertice_prima_h, Vertice_prima_k,\
           Vertice_sec_h, Vertice_sec_k, Vertice_sec_prima_h, Vertice_sec_prima_k, Foco_h, Foco_k, Foco_prima_h, Foco_prima_k, Lado_recto, excentricidad

@app.post("/desarrollador4")
def desarrollar_hiperbola(A, B, D, E, F, orintacion, H, K):

    Centro_h = -1 * D / (2 * A)
    Centro_k = -1 * E / (2 * B)
    if D == 0 and E == 0 and F >= 0:
        return None
    elif orintacion == "vertical":
        a_menor = 1 / ((abs(B) / ((-1 * F) + ((D ** 2) / (4 * A)) + ((E ** 2) / (4 * B)))) ** (1 / 2))
        b_mayor = 1 / ((abs(A) / ((-1 * F) + ((D ** 2) / (4 * A)) + ((E ** 2) / (4 * B)))) ** (1 / 2))
        c_focal = ((a_menor ** 2) + (b_mayor ** 2)) ** (1 / 2)

        Vertice_h = Centro_h
        Vertice_k = Centro_k + a_menor
        Vertice_prima_h = Centro_h
        Vertice_prima_k = Centro_k - a_menor

        Foco_h = Centro_h
        Foco_k = Centro_k + c_focal
        Foco_prima_h = Centro_h
        Foco_prima_k = Centro_k - c_focal

    else:
        a_menor = 1 / ((abs(A) / ((-1 * F) + ((D ** 2) / (4 * A)) + ((E ** 2) / (4 * B)))) ** (1 / 2))
        b_mayor = 1 / ((abs(B) / ((-1 * F) + ((D ** 2) / (4 * A)) + ((E ** 2) / (4 * B)))) ** (1 / 2))
        c_focal = ((a_menor ** 2) + (b_mayor ** 2)) ** (1 / 2)

        Vertice_h = Centro_h + a_menor
        Vertice_k = Centro_k
        Vertice_prima_h = Centro_h - a_menor
        Vertice_prima_k = Centro_k

        Foco_h = Centro_h + c_focal
        Foco_k = Centro_k
        Foco_prima_h = Centro_h - c_focal
        Foco_prima_k = Centro_k

    Lado_recto = (2 * (b_mayor ** 2)) / a_menor
    excentricidad = c_focal / a_menor

    return a_menor, b_mayor, c_focal, Centro_h, Centro_k, Vertice_h, Vertice_k, Vertice_prima_h, Vertice_prima_k,\
        Foco_h, Foco_k, Foco_prima_h, Foco_prima_k, Lado_recto, excentricidad
@app.post("/redondeador_de_tuplas")
def redondear_tupla(tupla_inicial, numero_de_decimales):
    try:
       tupla2 = ()
       for numero in tupla_inicial:
           numero = round(numero, numero_de_decimales)
           aux = ("xd", numero)
           tupla2 = tupla2 + aux

       lista = list(tupla2)
       lista2 = []

       for numero in lista:
          if numero != "xd":
             lista2.append(numero)
       tupla_final = tuple(lista2)
       return tupla_final
    except TypeError:
        return None

@app.post("/resuleve_matriz_para_rotar_conica")
def resolviendo_matriz_M(matriz):
    desarrollo = [1, (matriz[0][0] * -1) + (matriz[1][1] * -1),
                  (matriz[0][0] * matriz[1][1]) - (matriz[0][1] * matriz[1][0])]
    A = desarrollo[0]
    B = desarrollo[1]
    C = desarrollo[2]
    lamda1 = ((B * (-1)) + ((B ** (2)) - (4 * A * C)) ** (1 / 2)) / (2 * A)
    lamda2 = ((B * (-1)) - ((B ** (2)) - (4 * A * C)) ** (1 / 2)) / (2 * A)

    matriz[0][0] -= lamda1
    matriz[1][1] -= lamda1

    if matriz[0][0] == 0 and matriz[0][1] == 0:
        numerador, denominador = simplificador_de_fracciones(matriz[1][1], matriz[1][0] * (-1))
        if numerador < 0 and denominador < 0:
            numerador *= (-1)
            denominador *= (-1)
        if numerador == 0:
            vector1 = [0, 1]
        elif denominador == 0:
            vector1 = [1, 0]
        else:
            vector1 = [numerador, denominador]
    elif matriz[1][0] == 0 and matriz[1][1] == 0:
        numerador, denominador = simplificador_de_fracciones(matriz[0][1], matriz[0][0] * (-1))
        if numerador < 0 and denominador < 0:
            numerador *= (-1)
            denominador *= (-1)
        if numerador == 0:
            vector1 = [0, 1]
        elif denominador == 0:
            vector1 = [1, 0]
        else:
            vector1 = [numerador, denominador]
    else:
        numerador, denominador = simplificador_de_fracciones(matriz[0][1], matriz[0][0] * (-1))
        if numerador < 0 and denominador < 0:
            numerador *= (-1)
            denominador *= (-1)
        if numerador == 0:
            vector1 = [0, 1]
        elif denominador == 0:
            vector1 = [1, 0]
        else:
            vector1 = [numerador, denominador]

    matriz[0][0] += lamda1 - lamda2
    matriz[1][1] += lamda1 - lamda2

    if matriz[0][0] == 0 and matriz[0][1] == 0:
        numerador, denominador = simplificador_de_fracciones(matriz[1][1], matriz[1][0] * (-1))
        if numerador < 0 and denominador < 0:
            numerador *= (-1)
            denominador *= (-1)
        if numerador == 0:
            vector2 = [0, 1]
        elif denominador == 0:
            vector2 = [1, 0]
        else:
            vector2 = [numerador, denominador]
    elif matriz[1][0] == 0 and matriz[1][1] == 0:
        numerador, denominador = simplificador_de_fracciones(matriz[0][1], matriz[0][0] * (-1))
        if numerador < 0 and denominador < 0:
            numerador *= (-1)
            denominador *= (-1)
        if numerador == 0:
            vector2 = [0, 1]
        elif denominador == 0:
            vector2 = [1, 0]
        else:
            vector2 = [numerador, denominador]
    else:
        numerador, denominador = simplificador_de_fracciones(matriz[0][1], matriz[0][0] * (-1))
        if numerador < 0 and denominador < 0:
            numerador *= (-1)
            denominador *= (-1)
        if numerador == 0:
            vector2 = [0, 1]
        elif denominador == 0:
            vector2 = [1, 0]
        else:
            vector2 = [numerador, denominador]

    escalar1 = ((vector1[0] ** 2) + (vector1[1] ** 2)) ** (1 / 2)
    escalar2 = ((vector2[0] ** 2) + (vector2[1] ** 2)) ** (1 / 2)

    vector1[0] /= escalar1
    vector1[1] /= escalar1

    vector2[0] /= escalar2
    vector2[1] /= escalar2

    if round((vector1[0] * vector2[1]) - (vector1[1] * vector2[0]),1) == 1.0:
        matriz_P = [[vector1[0], vector2[0]], [vector1[1], vector2[1]]]
        matriz_D = [[lamda1, 0], [0, lamda2]]
    else:
        matriz_P = [[vector2[0], vector1[0]], [vector2[1], vector1[1]]]
        matriz_D = [[lamda2, 0], [0, lamda1]]
    #print(matriz_P, matriz_D)
    return matriz_P, matriz_D

@app.post("/rotador_de_conicas")
def rotar_conica(A, B, C, D, E):
    matriz_M = [[A, C/2], [C/2, B]]
    matriz_P, matriz_D = resolviendo_matriz_M(matriz_M)

    A = matriz_D[0][0]
    B = matriz_D[1][1]
    C = 0
    D = (D * matriz_P[0][0]) + (E * matriz_P[1][0])
    E = (D * matriz_P[0][1]) + (E * matriz_P[1][1])

    return A, B, C, D, E

@app.post("/traslada_conicas")
def traslacion_de_conica(A, B, C, D, E, F):
    K = (((C * D) / (2 * A)) - E) / ((2 * B) - ((C ** 2) / (2 * A)))
    H = ((-1 * D) - (C * K)) / (2 * A)
    centro = [H, K]

    F += (C * H * K) + (B * (K ** 2)) + (A * (H ** 2)) + (D * H) + (E * K)
    D = 0
    E = 0

    return A, B, C, D, E, F, H, K

def geo_analitica():    #Ax^2 + By^2 + Dx + Ey + F = 0

    termino_A = 0
    termino_B = 0
    termino_C = 0
    termino_D = 0
    termino_E = 0
    termino_F = 0
    H = ""
    K = ""
    ecuacion_rotada = ""
    ecuacion = request.form.get("ecuacion_en_bruto")

    mi_ecuacion, ecuacion_publica = organizar_ecuacion_conica(ecuacion)

    if mi_ecuacion == ecuacion_publica:
        mi_figura_conica = "no existe"
        return render_template("analitica.html", ecuacion=ecuacion, mi_figura_conica=mi_figura_conica)
    if mi_ecuacion == 1 and ecuacion_publica == 2:
        mi_figura_conica = "decimal"
        return render_template("analitica.html", ecuacion=ecuacion, mi_figura_conica=mi_figura_conica)


    if ecuacion_publica[0][0] == "+":
        del ecuacion_publica[0][0]
    ecuacion = ""
    for termino in ecuacion_publica:
        for caracter in termino:
            ecuacion += str(caracter)


    numero_de_terminos = len(mi_ecuacion)

    ecuacion = re.sub(r"\^(\d+)", r"<sup> \1 </sup>", ecuacion)

    for iterador in range(0, numero_de_terminos):   #mi_ecuacion es una lista de objetos
        if mi_ecuacion[iterador].especie == "x^2":
            termino_A += mi_ecuacion[iterador].coheficiente
        elif mi_ecuacion[iterador].especie == "y^2":
            termino_B += mi_ecuacion[iterador].coheficiente
        elif mi_ecuacion[iterador].especie == "xy" or mi_ecuacion[iterador].especie == "yx" :
            termino_C += mi_ecuacion[iterador].coheficiente
        elif mi_ecuacion[iterador].especie == "x":
            termino_D += mi_ecuacion[iterador].coheficiente
        elif mi_ecuacion[iterador].especie == "y":
            termino_E += mi_ecuacion[iterador].coheficiente
        elif mi_ecuacion[iterador].especie == "":
            termino_F += mi_ecuacion[iterador].coheficiente

    if termino_C != 0:
        mi_figura_conica = "no se puede procesar"
        return render_template("analitica.html", ecuacion=ecuacion, mi_figura_conica=mi_figura_conica)



    mi_figura_conica = identificar_figura_conica(termino_A, termino_B)

    if (termino_B == 0 and termino_E == 0) or (termino_A == 0 and termino_D == 0):
        mi_figura_conica = "no existe"
    elif mi_figura_conica == "circunferencia":
        if ecuacion_rotada != "":
            orientacion = re.sub(r"\^(\d+)", r"<sup> \1 </sup>","rotada a " + ecuacion_rotada + " inecesariamente")
        else:
            orientacion = ""
        atributos = desarrollar_circunferencia(termino_A, termino_B, termino_D, termino_E, termino_F, H, K)

        if atributos == None:
            mi_figura_conica = "no existe"
        else:
            atributos_redondeados = redondear_tupla(atributos, 3)
            if atributos_redondeados == None:
                mi_figura_conica = "complejo"
                return render_template("analitica.html", ecuacion = ecuacion, mi_figura_conica = mi_figura_conica)
            centro_h, centro_k, radio = atributos_redondeados
            return render_template("analitica.html", ecuacion = ecuacion, mi_figura_conica = mi_figura_conica,
                                   centro_h = centro_h, centro_k = centro_k, radio = radio, orientacion = orientacion)

    elif mi_figura_conica == "parabola":
        orientacion= ""

        if termino_A != 0:
            orientacion += "vertical"
        else:
            orientacion += "horizontal"
        atributos = desarrollar_parabola(termino_A, termino_B, termino_D, termino_E, termino_F, orientacion, H, K)
        if ecuacion_rotada != "":
            orientacion += re.sub(r"\^(\d+)", r"<sup> \1 </sup>","rotada a " + ecuacion_rotada)
        if atributos == None:
            mi_figura_conica = "no existe"
        else:
            atributos_redondeados = redondear_tupla(atributos, 3)
            if atributos_redondeados == None:
                mi_figura_conica = "complejo"
                return render_template("analitica.html", ecuacion = ecuacion, mi_figura_conica = mi_figura_conica)
            foco_h, foco_k, vertice_h, vertice_k, lado_recto, distancia_focal = atributos_redondeados
            return render_template("analitica.html", ecuacion = ecuacion, mi_figura_conica = mi_figura_conica,
                                   foco_h = foco_h, foco_k = foco_k, vertice_h = vertice_h,
                                   vertice_k = vertice_k, lado_recto = lado_recto, distancia_focal = distancia_focal, orientacion = orientacion)
    elif mi_figura_conica == "elipse":
        orientacion = ""

        if termino_A > termino_B:
            orientacion += "vertical"
        else:
            orientacion += "horizontal"
        atributos = desarrollar_elipse(termino_A, termino_B, termino_D, termino_E, termino_F, orientacion, H, K)
        if ecuacion_rotada != "":
            orientacion += re.sub(r"\^(\d+)", r"<sup> \1 </sup>"," rotada a " + ecuacion_rotada)
        if atributos == None:
            mi_figura_conica = "no existe"
        else:
            atributos_redondeados = redondear_tupla(atributos, 3)
            if atributos_redondeados == None:
                mi_figura_conica = "complejo"
                return render_template("analitica.html", ecuacion = ecuacion, mi_figura_conica = mi_figura_conica)
            semieje_mayor, semieje_menor, semieje_focal, Centro_h, Centro_k, Vertice_principal_h, Vertice_principal_k, \
            Vertice_principal_prima_h, Vertice_principal_prima_k, Vertice_sec_h, Vertice_sec_k, Vertice_sec_prima_h, Vertice_sec_prima_k,\
            Foco_h, Foco_k, Foco_prima_h, Foco_prima_k, Lado_recto, excentricidad = atributos_redondeados
            return render_template("analitica.html", ecuacion=ecuacion, mi_figura_conica=mi_figura_conica,
                                   semieje_mayor = semieje_mayor, semieje_menor = semieje_menor,
                                   semieje_focal = semieje_focal, Centro_h = Centro_h, Centro_k = Centro_k,
                                   Vertice_principal_h = Vertice_principal_h, Vertice_principal_k = Vertice_principal_k,
                                   Vertice_principal_prima_h = Vertice_principal_prima_h, Vertice_principal_prima_k = Vertice_principal_prima_k,
                                   Vertice_sec_h = Vertice_sec_h, Vertice_sec_k = Vertice_sec_k,
                                   Vertice_sec_prima_h = Vertice_sec_prima_h, Vertice_sec_prima_k = Vertice_sec_prima_k,
                                   Foco_h = Foco_h, Foco_k = Foco_k, Foco_prima_h = Foco_prima_h, Foco_prima_k = Foco_prima_k,
                                   Lado_recto = Lado_recto, excentricidad = excentricidad, orientacion = orientacion)
    elif mi_figura_conica == "hiperbola":
        orientacion = ""

        if termino_A < 0:
            orientacion += "vertical"
        else:
            orientacion += "horizontal"
        atributos = desarrollar_hiperbola(termino_A, termino_B, termino_D, termino_E, termino_F, orientacion, H, K)
        if ecuacion_rotada != "":
            orientacion += re.sub(r"\^(\d+)", r"<sup> \1 </sup>"," rotada a " + ecuacion_rotada)
        if atributos == None:
            mi_figura_conica = "no existe"
        else:
            atributos_redondeados = redondear_tupla(atributos, 3)
            if atributos_redondeados == None:
                mi_figura_conica = "complejo"
                return render_template("analitica.html", ecuacion = ecuacion, mi_figura_conica = mi_figura_conica)
            semieje_menor, semieje_mayor, semieje_focal, Centro_h, Centro_k, Vertice_principal_h, Vertice_principal_k, \
            Vertice_principal_prima_h, Vertice_principal_prima_k, \
            Foco_h, Foco_k, Foco_prima_h, Foco_prima_k, Lado_recto, excentricidad = atributos_redondeados
            return render_template("analitica.html", ecuacion=ecuacion, mi_figura_conica=mi_figura_conica,
                                   semieje_menor = semieje_menor, semieje_mayor = semieje_mayor, semieje_focal = semieje_focal,
                                   Centro_h = Centro_h, Centro_k = Centro_k, Vertice_principal_h = Vertice_principal_h, Vertice_principal_k = Vertice_principal_k,
                                   Vertice_principal_prima_h = Vertice_principal_prima_h, Vertice_principal_prima_k = Vertice_principal_prima_k,
                                   Foco_h = Foco_h , Foco_k = Foco_k, Foco_prima_h = Foco_prima_h, Foco_prima_k = Foco_prima_k,
                                   Lado_recto = Lado_recto, excentricidad = excentricidad, orientacion = orientacion)


    return render_template("analitica.html", ecuacion = ecuacion, mi_figura_conica = mi_figura_conica)
