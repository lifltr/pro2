from collections import defaultdict
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from daten import serie_speichern, serien_laden

app = Flask("Serien_Verwaltung")


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/serieAnlegen/", methods=['GET', 'POST'])
def serieAnlegen():
    if request.method == 'POST':

        name = request.form['Serie']
        serie = { "name":name, "genre": request.form.get('Genre'), "staffelanzahl": request.form['Staffelanzahl'],
                  "erscheinungsjahr": request.form['Erscheinungsjahr'], "bewertung": request.form.get('Bewertung')}

        serie_speichern(name, serie)

        return redirect(url_for("serien"))
    else:
        return render_template("index.html")

# Hier wird die Startseite "Serie Anlegen" erstellt. Sie enthält aus einem Formular.
#
# Nach dem man das Formular ausgefühlt hat,wird man auf die Seite "bibliothek" weitergeleitet, wo die Funktion "serien" ausgeführt wird.

@app.route("/bibliothek/", methods=['GET'])
def serien():
    serien = serien_laden()
    serien = auflisten(serien)
    return render_template("bibliothek.html", bibliothek=serien)

def auflisten(serien):
    serien_liste = ""
    for key, value in serien.items():
        zeile = str(key) + ": " + str(value["genre"]) + ", " + (value["staffelanzahl"]) + " Staffeln" + ", " + "Erscheinungsjahr: " +\
                (value["erscheinungsjahr"]) + ", " + "deine Bewertung: " +(value["bewertung"]) + "<br>"
        serien_liste += zeile


    return serien_liste

@app.route("/statistik/", methods=['GET'])
def statistik():
    serien = serien_laden()



    genre = defaultdict(list)
    durchschnitt = {}
    summe = 0
    maximum = None
    minimum = None

    for name, serie in serien.items():
        bewertung = int(serie["bewertung"])
        genre[serie["genre"]].append(bewertung)
        summe = summe + 1
        if not maximum or int(maximum["bewertung"]) < bewertung:
            maximum = serie
        if not minimum or int(minimum["bewertung"]) > bewertung:
            minimum = serie

    for key, items in genre.items():
        avg = sum(items) / len(items)
        durchschnitt[str(key)] = { "durchschnitt": avg }

    statistik = { "durchschnitt":durchschnitt, "summe":summe, "maximum":maximum, "minimum":minimum }
    return render_template("statistik.html", statistik=statistik)



if __name__ == "__main__":
    app.run(debug=True, port=5000)