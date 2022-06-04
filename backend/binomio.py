import re

from flask import Flask, render_template, request

from backend import mendel, logicaProposicional, figurasConicas

app = Flask(__name__, template_folder="../templates")


@app.get("/")
def index():
    return render_template("home.html")

@app.get("/newton")
def newton_binomio():
    return render_template("newton.html")

@app.get("/analitica")
def analitica():
    return render_template("analitica.html")

@app.post("/analitica")
def geometria_analitica():
    return figurasConicas.geo_analitica()
@app.get("/logica")
def logica():
    return render_template("logica.html")

@app.post("/logica")
def desarrolla_la_logica():
    return logicaProposicional.desarrolla_logica()

@app.get("/mendel")
def leyes_mendel_inicial():
    return render_template("mendel.html")

@app.post("/mendel")
def leyes_mendelianas():
    return mendel.leyes_mendel()

@app.post("/pascal")
def coeficiente(t):
    # t = int(request.form.get("t"))
    piso = [1, 1]
    fila = [1]
    fila = piso[:]

    i = 0
    j = 1

    while (j < t):
        fila = piso[:]
        piso = [1, 1]

        for i in range(0, j):
            x = fila[i] + fila[i + 1]
            piso.insert(1, x)
            i += 1

        j += 1
    return piso


@app.post("/binomio")
def binomio():

    global miSigno
    primer_termino = str(request.form.get("primer_termino"))
    signito = str(request.form.get("signito"))

    if signito == "None":
        signito = "+"
    else:
        signito = "-"

    segundo_termino = str(request.form.get("segundo_termino"))
    exponente = float(request.form.get("exponente"))
    exponente = int(exponente)
    num = float(request.form.get("num"))
    num = int(num)

    if exponente < 0:
        Binomio = "No existe"
        miTermino = "Inexistente"
        posicion_termino = ""
        binomio_a_desarrollar = "No existe binomio de newton para exponentes negativos"
    else:

        global miSigno
        binomio_a_desarrollar = "(" + str(primer_termino) +" " + str(signito) + " " + str(segundo_termino) + ")^" + str(exponente)
        miTermino = 0
        termino = len(coeficiente(exponente))
        posicion_termino = num
        num = termino - num
        Binomio = ""


        if signito == "-":
            if num % 2 == 0 and exponente % 2 != 0:
                miSigno = "- "
            elif num % 2 == 0 and exponente % 2 == 0:
                miSigno = "+ "
            elif exponente % 2 != 0:
                miSigno = "+ "
            elif exponente % 2 == 0:
                miSigno = "- "

        else:
            miSigno = "+ "

        for i, j, k in zip(range(termino), range(exponente, -1, -1), range(termino, 0, -1)):

            if signito == "-" and exponente % 2 != 0:
                if k % 2 == 0 and k != 1:
                    signo = " - "
                elif k == 1:
                    signo = " "
                else:
                    signo = " + "


            elif signito == "-" and exponente % 2 == 0:
                if k % 2 == 0 and k != 1:
                    signo = " + "
                elif k == 1:
                    signo = " "
                else:
                    signo = " - "

            else:
                if k == 1:
                    signo = " "
                else:
                    signo = " + "

            if k == num + 1:

                if j == 0:
                    Binomio += "(" + str(segundo_termino) + ")" + "^" + str(i) + signo
                    miTermino = "(" + str(segundo_termino) + ")" + "^" + str(i)

                elif i == 0:
                    Binomio += "(" + str(primer_termino) + ")" + "^" + str(j) + signo
                    miTermino = "(" + str(primer_termino) + ")" + "^" + str(j)

                elif j == 1 and i == 1:
                    Binomio += str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "* " + "(" + str(segundo_termino) + ")" + signo
                    miTermino = str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "* " + "(" + str(segundo_termino) + ")"

                elif j == 1:
                    Binomio += str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "* " + "(" + str(segundo_termino) + ")" + "^" + str(i) + signo
                    miTermino = str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "* " + "(" + str(segundo_termino) + ")" + "^" + str(i)

                elif i == 1:
                    Binomio += str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "^" + str(j) + "* " + "(" + str(segundo_termino) + ")" + signo
                    miTermino = str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "^" + str(j) + "* " + "(" + str(segundo_termino) + ")"

                else:
                    Binomio += str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "^" + str(j) + "* " + "(" + str(segundo_termino) + ")" + "^" + str(i) + signo
                    miTermino = str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "^" + str(j) + "* " + "(" + str(segundo_termino) + ")" + "^" + str(i)
            else:

                if j == 0:
                    Binomio += "(" + str(segundo_termino) + ")" + "^" + str(i) + signo
                elif i == 0:
                    Binomio += "(" + str(primer_termino) + ")" + "^" + str(j) + signo
                elif j == 1 and i == 1:
                    Binomio += str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "* " + "(" + str(segundo_termino) + ")" + signo
                elif j == 1:
                    Binomio += str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "* " + "(" + str(segundo_termino) + ")" + "^" + str(i) + signo
                elif i == 1:
                    Binomio += str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "^" + str(j) + "* " + "(" + str(segundo_termino) + ")" + signo
                else:
                    Binomio += str(coeficiente(exponente)[k - 1]) + "* " + "(" + str(primer_termino) + ")" + "^" + str(j) + "* " + "(" + str(segundo_termino) + ")" + "^" + str(i) + signo

        if miTermino != 0:
            miTermino = miSigno + miTermino
            miTermino = re.sub(r"\^(\d+)", r"<sup> \1 </sup>", miTermino)

        else:
            miTermino = "Inexistente en el desarrollo de este binomio"

    if exponente == 0 and num == 1:
        Binomio = "1"
        miTermino = "1"
    if exponente == 0:
        Binomio = "1"

    if exponente == 1:
        Binomio = str(primer_termino) + " " + str(signito) + " " + str(segundo_termino)


    else:
        Binomio = re.sub(r"\^(\d+)", r"<sup> \1 </sup>", Binomio)
        Binomio = re.sub(r"\*", r"", Binomio)

    binomio_a_desarrollar = re.sub(r"\^(\d+)", r"<sup> \1 </sup>", binomio_a_desarrollar)


    return render_template("newton.html",exponente = exponente, binomio_inicial = binomio_a_desarrollar, Binomio=Binomio, Termino_buscado=miTermino, numero=posicion_termino)

if __name__ == '__main__':
    app.run()
