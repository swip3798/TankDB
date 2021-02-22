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
