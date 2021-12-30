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
        serie = { "name":name, "genre": request.form['Genre']
                  , "staffelanzahl": request.form['Staffelanzahl'], "erscheinungsjahr": request.form['Erscheinungsjahr'], "bewertung": request.form['Bewertung']}

        serie_speichern(name, serie)

        return redirect(url_for("serien"))
    else:
        return render_template("index.html")


@app.route("/serien/", methods=['GET'])
def serien():
    serien = serien_laden()
    serien = auflisten(serien)
    return render_template("Serie_angelegt.html", bibliothek=serien)


@app.route("/statistik/", methods=['GET'])
def statistik():
    serien = serien_laden()
    genre = defaultdict(list)
    durchschnitt = {}
    for key, serie in serien.items():
        bewertung = int(serie["bewertung"])
        genre[serie["genre"]].append(bewertung)

    for key, items in genre.items():
        avg = sum(items) / len(items)
        durchschnitt[str(key)] = { "durchschnitt": avg }

    return render_template("statistik.html", statistik=durchschnitt)

def auflisten(serien):
    serien_liste = ""
    for key, value in serien.items():
        zeile = str(key) + ": " + str(value["genre"]) + ", " + (value["staffelanzahl"]) + " Staffeln" + ", " + "Erscheinungsjahr: " +\
                (value["erscheinungsjahr"]) + ", " + "deine Bewertung: " +(value["bewertung"]) + "<br>"
        serien_liste += zeile


    return serien_liste


@app.route("/bewertung/", methods=['GET'])
def bewertung():
    serien = serien_laden()

    return render_template("bewertung.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)