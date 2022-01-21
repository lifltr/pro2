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
# diese Seite wurde erstellt, dass nicht immer der url angepasst werden muss (kopie von index.html)

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

# Hier wird die Startseite "Serie Anlegen" erstellt. Sie besteht aus einem Formular.
# durch die funktion serieAnlegen werden die Daten den richtigen Übertitel zugewiesen, so dass die Daten in einem Dictionary gespeichert werden können.
# Nach dem man das Formular ausgefühlt hat, wird man auf die Seite "bibliothek" weitergeleitet, wo die Funktion "serien" ausgeführt wird.

@app.route("/bibliothek/", methods=['GET'])
def serien():
    serien = serien_laden()
    serien = auflisten(serien)
    return render_template("bibliothek.html", bibliothek=serien)

# hier werden die Daten (serien_laden) welche in daten.py gespeichert werden aufgelistet wie es in der Funktion auflisten(serien) beschrieben wird.
# Dies funktioniert nur wegen der Funktion serien_laden() im daten.py file.

def auflisten(serien):
    serien_liste = ""
    for key, value in serien.items():
        zeile = str(key) + ": " + str(value["genre"]) + ", " + (value["staffelanzahl"]) + " Staffel(n)" + ", " + "Erscheinungsjahr: " +\
                (value["erscheinungsjahr"]) + ", " + "deine Bewertung: " +(value["bewertung"]) + "<br>"
        serien_liste += zeile


    return serien_liste

#hier wird definiert, wie die Serie formatiert werden soll.

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

# mit dem heruntergeladenen defaultdict wir eine leere Liste erstellt, dass einfacher mit den daten gerechnet werden kann
# das Attrtibut Bewertung wird aus dem dictionary (serie) herausgenommen und als Bewertung definiert.
# wenn die Bewertung existiert und grösser als die bereits bestehende ist wird diese neu als maximum/minimum definiert.


if __name__ == "__main__":
    app.run(debug=True, port=5000)