**KIbarDok**

**Vorgehensweise zur Extrahierung der Hauptmerkmale der Dateien und deren
Zuordnung der entsprechenden Objektnummer**

**Vorbereitungen (Stand 17.05.2021)**

- Tika wird mithilfe eines Docker Containers ausgeführt. Falls noch nicht vorhanden, bitte zuerst Docker herunterladen und installieren: https://docs.docker.com/docker-for-windows/install/ . Um den Tika Server auf Docker laufen zu lassen:

  1. "Pull the image" mit: docker pull logicalspark/docker-tikaserver
  2. "Run the image" mit: docker run -d -p 9998:9998 logicalspark/docker-tikaserver
     (andere Ports müssten auch funktionieren, aber 9998 ist default)

- Bibliotheken unter requirements.txt müssen installiert werden

- Input data: Die Datei Input\input.txt kann genutzt werden, um die Input-Daten einzugeben. Die Datei ist noch sehr primitiv, und die Zeilennummer der Angaben darf nicht ohne weiteres verändert werden. Dies kann in der Zukunft selbstverständlich verbessert werden.

- Die Datei extractMetadata.py entnimmt die Input-Informationen aus Input\input.txt, und extrahiert die Metadaten. Diese werden dann in dem Ordner/der Datei gespeichert, die in der Input-Datei angegeben wurde

** ------------ Alte Beschreibungen: ------------ **

**findObjNr.ipynb (Stand 08.03.2021)** für Christian zum Test in Doc-Dateien. Dieser Skript nutzt die aktuellste Denkmal-Dict, und somit wenn nötig auch die Sachbegriffe in Kombination mit Strassenname, um eine trifftige Objektnummer zu finden.

**vorhabenExtrahierung.ipynb (Stand 01.03.2021)**

**BENÖTIGTE (externe) BIBLIOTHEKEN**

- spacy==3.0.1
- pyspellchecker==0.6.1
- HanTa==0.2.0
- python-docx==0.8.10
- pywin32==227
- regex==2020.11.13
- tika==1.24

**Details**
Bitte achtet darauf, den Pfad zu den Dateien anzupassen (# Pfad zu den Dateien). Auch der Output-Pfad (# Dataframe in Excel-Tabelle speichern) soll angepasst werden, wenn eine Excel-Datei mit den Ergebnissen im Anschluss gespeichert werden soll.

**objktNrFinder_preview.ipynb (Stand 19.02.2021)**

**BENÖTIGTE BIBLIOTHEKEN**

- json
- os
- **tika**
- difflib
- string
- **re (regex)**
- **spacy**
- numpy
- **pdf2image**
- **pillow**
- **pytesseract**
  (Programmiersprache: Python)

Die fettmarkierten Bibliotheken werden für die Extrahierung der Hauptmerkmale
verwendet, und werden im folgenden Text genannt.

**VORBEREITUNGEN**

1.  Dateienname wird maschinenlesbar gemacht (Leerzeichen entfernt,
    Sonderzeichen „/(„ werden entfernt)

2.  Das Denkmal-Dictionary wird eingelesen (Bibliothek: tika). Eine Liste mit
    allen Adressen unter einer Objektnummer wird ausgeschrieben:

    ![](https://github.com/larissamsg/Denkmal-Berlin/blob/main/bilder/vorbereitung_denkmalliste.jpg)

3.  Ein Dictionary mit allen Behörden und zugehörigen Adressen wird geladen
    (Bibliothek: json).

4.  Alle im Ordner vorhandenen Vorhaben werden in einer Liste gespeichert. Das
    Vorhaben wird durch die Suche nach der Kombination „Vorhaben: „, welche in
    offiziellen Dokumenten zu finden ist:

    ![](https://github.com/larissamsg/Denkmal-Berlin/blob/main/bilder/vorbereitung_vorhaben.jpg)

**HAUPTSCHLEIFE**

In der Hauptschleife werden Objektnummer, Adresse, Vorhaben in den Dateien
identifiziert, wenn der Inhalt der Dokumente das erlaubt.

1.  Jedes Dokument wird eingelesen, und dessen Inhalt wird extrahiert
    (Bibliothek: tika, pdf2image, pillow, pytesseract). Dafür gibt es zwei
    Methoden:

    1.  Wenn der Text direkt eingelesen werden kann, wird dies mit einem
        üblichen Parser getan

    2.  Bei eingescannten Dateien muss das „Bild“ zuerst einmal eingelesen
        werden, und durch OCR (optical character recognition) wird der Text
        daraus entnommen

2.  In der dargestellten Reihenfolge wird jedes Dokument gescannt nach
    (Bibliothek: regex und eigene ausgearbeiteten regex-Ausdrücke):

    1.  Objektnummer

    2.  Adresse

    3.  Datum

    4.  Postleitzahl

3.  Bei der Objektnummer wird wie folgt vorgegangen (Bibliothek: regex und
    eigene ausgearbeiteten regex-Ausdrücke, spacy):

    1.  Wenn eine Objektnummer im Dokument gefunden wurde, wird diese Variante
        vorgezogen

    2.  Wenn keine Objektnummer im Dokument gefunden werden konnte, aber eine
        Adresse vorhanden ist, wird die Objektnummer durch die Adresse bestimmt

    3.  Andernfalls wird die Objektnummer anhand des Vorhabens und Ort bestimmt
        (s. unten)

- Manchmal sind in einem Dokument mehrere Objektnummer vorhanden. Wenn das der
  Fall ist, wird als finale Objektnummer der Datei diejenige zugeordnet, die
  am häufigsten auftaucht. Alle vorhandenen Objektnummer werden in jedem Fall
  in einer weiteren Variabel festgehalten.

1.  Wenn eine Adresse (oder mehrere) vorhanden ist, wird geprüft, ob mindestens
    eine davon die Adresse einer Behörde entspricht.

2.  Jede Datei wird einem „Ort“ zugeordnet (z. B. „Akazienhof“ oder
    „Wilhelminenhofstraße“; Bibliothek: spacy). Das wird ggf. im übernächsten
    Schritt, zusammen mit dem identifizierten Vorhaben, genutzt, um eine
    Objektnummer für die Datei zu finden, falls noch keine dafür zugeordnet
    werden konnte.

3.  Jede Datei wird einem der im Ordner vorhandenen Vorhaben zugeordnet, in dem
    die Worte im Dateieninhalt mit den Vorhaben verglichen wird. Das Vorhaben
    mit der höchsten Übereinstimmung wird genommen.

4.  Wenn der entsprechenden Datei noch keiner Objektnummer zugeordnet werden
    konnte, wird dies hier anhand des identifizierten Vorhabens und Ortes getan.

    ![](https://github.com/larissamsg/Denkmal-Berlin/blob/main/bilder/hauptschleife_vorhabenloc.jpg)

5.  Die extrahierten Informationen werden in einem Dictionary gespeichert, was
    anschließend in einer Excel-Datei o.a. gespeichert werden kann.

    ![](https://github.com/larissamsg/Denkmal-Berlin/blob/main/bilder/hauptschleife_filesdict.jpg)
