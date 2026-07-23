import json
import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php"

PARAMS = {
    "saison": "2026/2027",
    "codent": "LIIDF",     # code de la ligue 
    "poule": "2MC",
    "calend": "COMPLET",
    "equipe": "1"

}

MATCHES_FILE = Path("matchs.json")

def scrap_matches (params = PARAMS):

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
    """Sauvegarde les matchs dans un fichier JSON (à lire depuis ton site web)."""
    path.write_text(json.dumps(matches, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    matches = scrap_matches()
    print(f"{len(matches)} matchs trouvés pour la saison {PARAMS['saison']}.\n")

    save_cache(matches)
    print(f"Calendrier sauvegardé dans {MATCHES_FILE.resolve()}\n")

""" nm = next_match(matches)
    if nm:
        print("Prochain match :")
        print(f"  {nm['domicile']} vs {nm['exterieur']}")
        print(f"  le {nm['date']} à {nm['heure']}")
        print(f"  Salle : {nm['salle']}")
    else:
        print("Aucun match à venir dans le calendrier récupéré.")
"""
