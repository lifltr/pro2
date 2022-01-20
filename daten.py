import json

def speichern(datei, key, value):
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    datei_inhalt[str(key)] = value


    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file, indent=4)

# hier wird die Funktion speichern erstellt. Die Daten werden in einem json file gespeichert.
# Falls es noch keine Einträge hat, wird ein leeres dictionary erstellt.


def serie_speichern(name, serie):
    speichern("serien.txt", name, serie)

# die gespeicherten Daten werden in einem txt file gespeichert. Das Dictionary Serie ist in dem Dictionary Name gespeichert.

def serien_laden():
    datei_name = "serien.txt"

    try:
        with open(datei_name) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt

# diese Funktion erlaubt es die Daten aus dem json File abzurufen. Dies wird in der HTML Seite "Bibliothek" verwendet.