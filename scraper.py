import json
import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php"

PARAMS = {
    "saison": "2026/2027",
    "codent": "PTIDF95",
    "poule": "ARO",
    "calend": "COMPLET",
    "equipe": "5",
}

MATCHES_FILE = Path("matches.json")
ICS_FILE = Path("calendrier.ics")

VTIMEZONE = [
    "BEGIN:VTIMEZONE",
    "TZID:Europe/Paris",
    "BEGIN:DAYLIGHT",
    "TZOFFSETFROM:+0100",
    "TZOFFSETTO:+0200",
    "TZNAME:CEST",
    "DTSTART:19700329T020000",
    "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU",
    "END:DAYLIGHT",
    "BEGIN:STANDARD",
    "TZOFFSETFROM:+0200",
    "TZOFFSETTO:+0100",
    "TZNAME:CET",
    "DTSTART:19701025T030000",
    "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU",
    "END:STANDARD",
    "END:VTIMEZONE",
]


def scrap_matches(params=PARAMS):
    resp = requests.get(BASE_URL, params=params, timeout=15)
    resp.encoding = "iso-8859-1"

    soup = BeautifulSoup(resp.text, "html.parser")
    matches = []

    # Chaque ligne de match a ce bgcolor précis dans le HTML du site.
    for row in soup.find_all("tr", bgcolor="#EEEEF8"):
        cells = row.find_all("td")
        if len(cells) < 8:
            continue  # ligne incomplète, on ignore

        code = cells[0].get_text(strip=True)
        date_str = cells[1].get_text(strip=True)
        heure = cells[2].get_text(strip=True)
        domicile = cells[3].get_text(strip=True)
        exterieur = cells[5].get_text(strip=True)
        salle = cells[7].get_text(strip=True)

        try:
            date = datetime.datetime.strptime(date_str, "%d/%m/%y")
        except ValueError:
            continue  # format de date inattendu, on ignore la ligne

        matches.append(
            {
                "code": code,
                "date": date.strftime("%Y-%m-%d"),
                "heure": heure,
                "domicile": domicile,
                "exterieur": exterieur,
                "salle": salle,
            }
        )

    return matches


def save_cache(matches: list[dict], path: Path = MATCHES_FILE) -> None:
    path.write_text(json.dumps(matches, ensure_ascii=False, indent=2), encoding="utf-8")


def ics_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", " ")
    )


def save_ics(matches: list[dict], path: Path = ICS_FILE) -> None:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Volley FFVB//FR",
        "CALSCALE:GREGORIAN",
        "X-WR-CALNAME:Volley",
        "X-WR-TIMEZONE:Europe/Paris",
        "REFRESH-INTERVAL;VALUE=DURATION:PT6H",
        "X-PUBLISHED-TTL:PT6H",
    ]
    lines += VTIMEZONE

    for m in matches:
        heure = m["heure"].replace("H", ":").replace("h", ":")
        try:
            debut = datetime.datetime.strptime(f"{m['date']} {heure}", "%Y-%m-%d %H:%M")
        except ValueError:
            continue  # heure absente ou illisible, on ignore le match
        fin = debut + datetime.timedelta(hours=2)

        lines += [
            "BEGIN:VEVENT",
            f"UID:{m['code']}@ffvb",
            # DTSTAMP fixe : évite un commit quotidien inutile
            "DTSTAMP:20260101T000000Z",
            f"DTSTART;TZID=Europe/Paris:{debut:%Y%m%dT%H%M%S}",
            f"DTEND;TZID=Europe/Paris:{fin:%Y%m%dT%H%M%S}",
            f"SUMMARY:{ics_escape(m['domicile'] + ' - ' + m['exterieur'])}",
            f"LOCATION:{ics_escape(m['salle'])}",
            "END:VEVENT",
        ]

    lines.append("END:VCALENDAR")
    path.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")


if __name__ == "__main__":
    matches = scrap_matches()
    print(f"{len(matches)} matchs trouvés pour la saison {PARAMS['saison']}.\n")

    save_cache(matches)
    save_ics(matches)
    print(f"Calendrier sauvegardé dans {ICS_FILE.resolve()}")
