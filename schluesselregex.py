# coding: utf-8
import re

# Check regex: https://pythex.org/
monthsShort="jan\.?|feb\.?|mär\.?|maer\.?|apr\.?|mai\.?|jun\.?|jul\.?|aug\.?|sept\.?|okt\.?|nov\.?|dez\.?"
monthsLong="januar|februar|märz|maerz|april|mai|juni|juli|august|september|oktober|november|dezember"
months="(" + monthsShort + "|" + monthsLong + "|[1-9]{1}|0[1-9]{1}|1[0-2]{1})"

days = "([0-3]{1}[0-9]{1}|[0-9]{1})"
years = "([1-2]{1}[0-9]{3}|[0-9]{1,2})"

ymd = '([\s|\n|\t])' + "([1-2]{1}[0-9]{3})" + '([.|/|\-|\s])(?:\s)?' + months + '([.|/|\-|\s|\n|\t])(?:\s)?' + days + '([\s|\n|\t|.])'
dmy = '([\s|\n|\t])' + days + '([.|/|\-|\s])(?:\s)?' + months + '([.|/|\-|\s|\n|\t])(?:\s)?' + years + '([\s|\n|\t|.])'


datum_dmy           =re.compile(dmy, re.IGNORECASE)  # regex day-month-year
datum_ymd           =re.compile(ymd, re.IGNORECASE)  # regex year-month-day

time             = re.compile('(\d{1,2}(?:.|:)\d{2} ?(?:Uhr\.?)?)', re.IGNORECASE)
email            = re.compile("([a-z0-9!#$%&'*+\/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)", re.IGNORECASE)
adresse_alternative = re.compile('[.\w-]{1,20}?(?:\s)?(?:strasse|str.|str|straße|allee|weide|Shof|weg|platz|damm|berg|promenade)\W?(?=\s|$) \d{1}(?:\w{1,2}\.?)?(?:-|/\.?)?(?:\w{1,3}\.?)?', re.IGNORECASE)

adresse          = re.compile('[.\w-]{1,20}?(?:\s)?(?:strasse|str.|str|straße|ufer|allee|hof|gestell|weide|anlage|gasse|graben|gestell|chaussee|wache|weg|platz|promenade|pforte|pfad|damm|tor|brücke|berg)\W??(?:\s)?\d{1}(?:\w{1,2}\.?)?(?:-|/\.?)?(?:\w{1,3}\.?)?', re.IGNORECASE)
# Strasse des 17. Juni, Platz des 18. März, Am Treptower Park, Am Neuen Palais

# Falls mehr Grundworte für die Adressenidentifizierung fehlt, können wir die schweizerische Liste nehmen:
# https://giswiki.hsr.ch/Grundw%C3%B6rter_bei_Strassennamen_in_St%C3%A4dten

plz              = re.compile(r'\b(1[0-4]{1}[0-9]{3})\b') # PLZ in Berlin: zwischen 10001-14330 (https://cebus.net/de/plz-bundesland.htm), hier wird erstmal vereinfacht und 10000-14999 berücksichtigt
objnr            = re.compile(r'\b(090[0-9]{5})\b')

behoerde = re.compile('(?:Charlottenburg-Wilmersdorf|Charlottenburg Wilmersdorf|Friedrichshain-Kreuzberg|Friedrichshain Kreuzberg|Lichtenberg|Marzahn-Hellersdorf|Marzahn Hellersdorf|Mitte|Neukölln|Pankow|Reinickendorf|Spandau|Steglitz-Zehlendorf|Steglitz Zehlendorf|Tempelhof-Schöneberg|Tempelhof Schöneberg|Treptow-Köpenick|Treptow Köpenick|Oberste Denkmalschutzbehörde|Landesdenkmalamt)', re.IGNORECASE)

adresseUnvollstaendig          = re.compile('[.A-Za-z0-9_äÄöÖüÜß-]{1,20}?(?:\s)?(?:straße|str.|str|strasse|ufer|allee|weide|hof|gestell|gasse|graben|gestell|chaussee|wache|weg|platz|promenade|pforte|pfad|damm|tor|brücke|berg)(?!\w)', re.IGNORECASE) #anlage|

# Weitere Wege ggf. Bezirke zu identifizieren
#|WEIßS-E|HALEN-D|WAIDM-G|REIND-G|ZEHLD-Ga|ALTGL-G|NIEDS-E|KAROW-Ga|MARZA-Ga|WILHE-D|REIND-D|BAUMS-G|WESTE-D|MITTE-G|NIKOL-G|TIERG-E|MALCH-G|STAAK-Ga|GATOW-D|WANNS-Ga|LANKW-E|AHOHS-Ga|MALCH-D|FRIED-E|BORWA-E|FRIFE-Ga|MALCH-E|OBERS-D|AHOHS-E|SCHMÖ-E|KARLH-D|LIFEL-E|FRHAI-D|NIKOL-D|NEU|FRIFE-G|HASEL-G|WILST-Ga|LIRAD-G|DAHLE-D|ROSET-G|STEGL-G|ZEHLD-G|MÜGGH-D|KÖPEN-G|NEUKÖ-G|FRHAI-G|MÄRKV-G|WAIDM-Ga|LANKW-G|JOHTH-G|GATOW-E|PANKO-D|PANKO-G, PAN|CHARL-Ga|TIERG-G|BOHND-G|PAN-G|RAHND-Ga|HASEL-D|TEGEL-Ga|SCHÖN-D|ROSET-Ga|KAULD-D|CHA-WILL|WEIßS-Ga|FALKB-G|BOHND-D|LIRAD-E|ALTTR-G|MARDF-E|PRENZ-E|SPAND-B|HAKEN-G|KÖP|KÖP-D|SCHMA-Ga|BORWA-D|BLANB-Ga|NEUKÖ-E|RUMBG-E|BUCKW-E|STEGL-Ga|RAHND-E|WAIDM-D|KREUZ-B|RAHND-D|BLANF-G|HERMD-Ga|CHARN-D|GESBR-B|TEMPH-E|MAR-HEL|WEDDG-Ga|GROPS-G|CHARL-E|FRIHG-E|FRIED-G|WILST-E|LÜBAR-G|PANKO-B|WILMD-G|BIESD-G|SPAND-E|MITTE-D|DAHLE-G|MÄRKV-D|WITTN-Ga|SPAND-D|ADLER-E|STE-ZEH|MOABI-Ga|WILST-D|STAAK-D|FRIFE-E|HEILS-D|FROHN-E|HEIND-E|MÜGGH-E|PRENZ-D|BOHND-E|WARTB-D|KARLH-G|NHOHS-D|GATOW-Ga|TEMPH-D|KAULD-Ga|ADLER-G|GRUNE-G|WILST-G|HEILS-E|MOABI-E|REIND-E|ALTGL-D|HEIND-D|WANNS-G|FROHN-G|HALEN-Ga|WARTB-E|FENPF-D|KAROW-D|GROPS-Ga|FRHAI-E|KAROW-G|KLADO-D|WESTE-Ga|LANKW-D|SPAND-Ga|BOHNSD-Ga|LIBER-D|WILHE-G|TEM-SCH|NIKOL-E|KLADO-G|FRI-KRE|ALTTR-G, TRE-KÖP|FRHAI-G, FRI-KRE|LIBER-Ga|WILMD-G, CHA-WIL|MITTE-B|MITTE-E|HALEN-E|JOHTH-D|REI|LIRAD-Ga|HEILS-G|REIND-Ga|WEIßS-D|KAROW-E|NEUKÖ-B|RAHND-G|WEIßS-B|FRHAI-Ga|FRZBU-G|KLADO-E|FRIFE-D|GROPS-D|BUCH-E|ZEHLD-D|LANKW-Ga|LIC|HALEN-G|BOHNSD-G|FRIHG-Ga|CHARN-E|TEMPH-Ga|HERMD-D|PLÄNT-D|LÜBAR-B|BIESD-E|NIEDS-G|KLADO-Ga|STEGL-E|MARFE-E|OBERS-G|BLANB-D|SCHMA-G|KAULD-G|BUCH-Ga|ROSET-E|REI-G|NIESW-G|WILMD-Ga|KAULD-E|SCHMA-E|PRENZ-Ga|CHA-WIL|ALTTR-D|HEILS-Ga|WESTE-G|KREUZ-G|LÜBAR-D|HERMD-G|WANNS-D|OBERS-E|KREUZ-E|GATOW-G|NIEDS-Ga|GESBR-Ga|MIT|CHARN-G|WANNS-E|FALFE-D|TRE-KÖP|BRITZ-D|TIERG-Ga|WEDDG-E|GRUNE-D|KONHÖ-G|WAIDM-E|BUCKW-G|OBERS-Ga|TEMPH-B|MARDF-G|FRZBU-E|MAHLD-G|RUMBG-D|GESBR-D|HELLD-D|LÜBAR-Ga|SIEME-D|PANKO-Ga|STEGL-D|NEUKÖ-Ga|FRZBU-D|NIKOL-Ga|SPA|MARDF-D|HEIND-G|PLÄNT-E|MARFE-D|TIERG-D|KÖPEN-D|LIFEL-D|BLANB-G|ALTTR-E|RUDOW-G|HEIND-Ga|MOABI-D|MITTE-Ga|PANKO-G|ZEHLD-E|CHARL-G|FROHN-D|KÖPEN-B|NEU-E|ADLER-D|LIFEL-G|KÖPEN-Ga|SIEME-Ga|AHOHS-B|SCHÖN-B|BLANF-Ga|TEGEL-G|BRITZ-Ga|MARZA-D|WITTN-D|BUCH-D|KÖP-G|BIESD-D|BRITZ-E|CHARL-D|ROSET-B|MARZA-G|KÖPEN-E|LIBER-G|LÜBAR-E|BUCKW-Ga|ALTGL-Ga|RUMBG-G|HELLD-E|SCHMÖ-G|MÜGGH-Ga|BORWA-G|TEGEL-E|TEMPH-G|BOHND-Ga|LIRAD-D|hansa-G|DAHLE-Ga|BLANF-E|MARFE-G|NIEDS-D|MAHLD-D|WILMD-E|STE-G|BAUMS-D|GRUNE-E|KONHÖ-D|NEUKÖ-D|ALTGL-E|RUDOW-D|ROSET-D|HANSA-G|BLANB-B|GRÜNA-D|SCHMÖ-D|HANSA-D|BRITZ-G|SCHÖN-Ga|FALKB-D|BUCH-G|SIEME-G|HAKEN-D|BLANB-E|MARFE-Ga|LIBER-E|KREUZ-Ga|NIESW-D|WEDDG-D|NEU-G|PANKO-E|ADLER-Ga|DAHLE-E|AHOHS-D|MARZA-E|FALFE-Ga|SCHÖN-G|MAHLD-Ga|KREUZ-D|PLÄNT-G|KARLH-E|BLANF-D|WIL-D|SCHMA-D|MARDF-Ga|MAHLD-E|BAUMS-E|STAAK-E|GRÜNA-G|WITTN-G|BUCH-B|BIESD-B|FALFE-G|BUCKW-B|FRIED-Ga|HERMD-E|WEIßS-G|FRIED-D|MOABI-G|SPAND-G|TEGEL-D|SCHÖN-E|PAN|STAAK-G|JOHTH-E|GRUNE-Ga|ALTTR-Ga|AHOHS-G|FRHAI-B|WILMD-D|BIESD-Ga|BUCKW-D|GESBR-E|FRIHG-G|BAUMS-Ga|FROHN-Ga|PRENZ-G|WITTN-E|GRÜNA-E|WEDDG-G|HAKEN-Ga|CHARN-Ga|FRIHG-D|LIFEL-Ga|WESTE-E|GESBR-G)'


regex_type = {
  "zeit"              : time,
  "email"             : email,
  "datum_dmy"           : datum_dmy,
  "datum_ymd"           : datum_ymd,
  "adresse"             : adresse,
  "adresseUnvollstaendig"           : adresseUnvollstaendig,
  "plz"               : plz,
  "objnr"             : objnr,
  "behoerde"             : behoerde
}

class regex:

  def __init__(self, obj, regex):
    self.obj = obj
    self.regex = regex

  def __call__(self, *args):
    def regex_method(text=None):
        xx = []
        for x in self.regex.findall(text or self.obj.text):
            if type(x) == tuple:
                xx.append(x)
            else:
                xx.append(x.strip())
        return xx
      #return [x.strip() for x in self.regex.findall(text or self.obj.text) if type(x) == tuple:]
    return regex_method

class getRegex(object):

    def __init__(self, text=""):
        self.text = text

        for k, v in list(regex_type.items()):
          setattr(self, k, regex(self, v)(self))

        if text:
            for key in list(regex_type.keys()):
                method = getattr(self, key)
                setattr(self, key, method())
