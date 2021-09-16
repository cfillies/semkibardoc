# semkibardoc

**KIbarDok**

###Vorbereitungen (Stand 16.09.2021)

- Tika wird mithilfe eines Docker Containers ausgeführt. Falls noch nicht vorhanden, bitte zuerst Docker herunterladen und installieren: https://docs.docker.com/docker-for-windows/install/ . Um den Tika Server auf Docker laufen zu lassen:

  1. "Pull the image" mit: docker pull logicalspark/docker-tikaserver
  2. "Run the image" mit: docker run -d -p 9998:9998 logicalspark/docker-tikaserver
     (andere Ports müssten auch funktionieren, aber 9998 ist default)

- Bibliotheken unter requirements.txt müssen installiert werden (python -m pip install -r requirements.txt)

- Zur Benutzung der mongoDB müssen Benutzername und Passwort in den Umgebungsvariablen des Nutzerkontos hinzugefügt werden
  1. Unter Windows: Start -> "Umgebungsvariablen für dieses Konto bearbeiten" -> Neu ...
  2. Name der Variablen: "KIBARDOC_USERNAME" (ohne Anführungszeichen), Wert der Variablen: <mongoDB username>
  3. Name der Variablen: "KIBARDOC_PASSWORD" (ohne Anführungszeichen), Wert der Variablen: <mongoDB password>

<!-- https://github.com/vgrem/Office365-REST-Python-Client -->

###Dann:
In `export2mongodb.py`:
  1. `data_folder` und `data_dir` an persönliche Verzeichnisse anpassen
  2. mongoDB `uri` anpassen
  3. `prepare_database()` füllt Datenbank mit benötigten Dokumenten
  4. `extract_contents()` extrahiert Textinhalt und Metadaten von Dokumenten in `datadir/datafolder`
  5. `extract_metadata()` analysiert Dateien auf Adressen, Daten, Denkmäler, ...

Load Data into mongodb
export2mongodb.py -> extractMetaData()