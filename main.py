from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from daten import serie_speichern, serien_laden

app = Flask("Serien_Verwaltung")


@app.route("/serieAnlegen/", methods=['GET', 'POST'])
def serieAnlegen():
    if request.method == 'POST':

        name = request.form['Serie']
        serie = { "name":name, "genre": request.form['Genre']
                  , "staffelanzahl": request.form['Staffelanzahl'], "erscheinungsjahr": request.form['Erscheinungsjahr']}

        serie_speichern(name, serie)

        return redirect(url_for("serien"))
    else:
        return render_template("index.html")

@app.route("/serien/", methods=['GET'])
def serien():
    serien = serien_laden()
    return render_template("Serie_angelegt.html", bibliothek=serien)

def auflisten():
    serien = serien_laden()

    serien_liste = ""
    for key, value in serien.items():
        zeile = str(key) + ": " + value + "<br>"
        serien_liste += zeile
        # fragen wieso die Darstellung nicht funktioniert

    return serien_liste


if __name__ == "__main__":
    app.run(debug=True, port=5000)