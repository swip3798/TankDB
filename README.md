# TankDB

Dieses Repository umfasst eine kleine Sammlung an Werkzeugen um eine MySQL Datenbank Tabelle mit Trainingsdaten von Spritpreisen zu befüllen. Die Trainingsdaten werden basiernd auf den historischen Preisänderungen von [Tankerkönig](https://creativecommons.tankerkoenig.de/) für einen beliebigen Zeitraum und eine beliebige Taktung generiert und anschließend in eine MySQL Datenbank Tabelle geschrieben. Mithilfe eines Cronjobs oder ähnlichem kann somit eine stets aktuelle Tabelle an Trainingsdaten gehalten werden.

## Vorraussetzungen
Benötigt werden:
* Python 3.5 oder höher
* Docker (Wenn MySQL nicht manuell installiert wird)

## Einrichtung
Zunächst muss das Git-Repository geklont werden und die Python Dependencys installiert werden.
```
git clone https://github.com/swip3798/TankDB.git
pip install -r requirements.txt
```
### Optional MySQL über Docker
Das Repository enthält eine docker-compose.yml zum schnellen Starten einer MySQL-Instanz. Wenn das gewünscht ist, muss jedoch zunächst eine ```.env``` Datei im TankDB Verzeichnis erstellt werden, in welcher die Passwörter für den Root-User und den normalen User festgelegt werden.  
Beispiel:
```
MYSQL_USER=exampleUser
MYSQL_ROOT_PASSWORD=xxxxxxxxxxxxxxxxxxxxxxxxx
MYSQL_PASSWORD=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
Daraufhin kann die MySQL-Instanz mit ```docker-compose up -d``` gestartet werden, erreichbar unter dem Port 5588. Der Port lässt sich in der Yaml-Datei anpassen.
### Tankerkönig History Daten
Anschließend wird das tankerkoenig-data Repository benötigt. Dieses findet man als Git-Repository [hier](https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data). Bitte beachtet die Nutzungsbediengungen für die Verwendung der History Daten. Zum aktuellen Zeitpunkt braucht das Repository etwas über 42GB Speicherplatz und muss übver 7GB beim Klonen herunterladen, Tendenz natürlich steigend.
```
git clone https://tankerkoenig@dev.azure.com/tankerkoenig/tankerkoenig-data/_git/tankerkoenig-data
```
### Python Skripte
Nun können Python-Skripte verwendet werden. Diese werden genutzt um zunächst Trainingsdaten zu generieren und diese in einer CSV Datei zu speichern. Danach wird der Inhalt der CSV-Datei in die Datenbank Tabelle eingefügt.
#### gentraindata.py
Dieses Skript generiert die Trainingsdaten auf Basis der historischen Daten aus dem tankerkoenig-data Repository. 
```
python gentraindata.py [-p P] [-d D] output_path
```
Der Parameter P beschreibt die Anzahl an Tagen, welche in den Trainingsdaten enthalten sein sollen, standardmäßig 7 Tage. Der Parameter D beschreibt die Anzahl der täglichen Datenpunkte pro Tankstelle, standardmäßig 24 für einen Datenpunkt pro Stunde. Der Output Path ist der Pfad, in welchem die CSV-Datei abgespeichert wird.
#### db_fill.py
Dieses Skript ließt den Inhalt der CSV-Datei und importiert diese in die Datenbank Tabelle.
```
python db_fill.py [-p PORT] input_path
```
Mit dem Parameter -p lässt sich der Port der MySQL-Instanz einstellen. Falls die MySQL-Instanz nicht unter localhost erreichbar ist, kann die URI im Skript angepasst werden (Zeile 18 in db_fill.py).
### Beispiel für Automatisierung
Für ein automatisches Aktualisieren der Datenbank empfiehlt sich das Einrichten eines Cronjobs oder etwas Vergleichbares. Die Daten im Tankerkönig Repository werden jeden Tag um 03:03 Uhr hochgeladen und können mit einem ```git pull``` heruntergeladen werden. Auf meinem Server habe ich ein Shell-Skript, welches das Tankerkönig Repository aktualisiert und anschließend beide Python-Skripte ausführt.
```shell
#!/bin/sh
cd /home/username/TankDB/tankerkoenig-data
git pull
cd ..
python3 gentraindata.py TrainData.csv
python3 db_fill.py TrainData.csv
```
Dieses Skript lasse ich über Crontab kurz nach 03:03 laufen. Auf diese Weise sind die Daten in meiner MySQL-Datenbank immer aktuell.
