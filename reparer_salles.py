import json
import subprocess
from pathlib import Path


FICHIERS = [
    "matches_SM-DEP.json",
    "matches_SF-TAV.json",
    "matches_SF-DEP.json",
]


def git_commits_fichier(path: str) -> list[str]:
    """Retourne les commits ayant modifié le fichier, du plus récent au plus ancien."""
    result = subprocess.run(
        ["git", "log", "--format=%H", "--", path],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()


def git_lire_fichier(commit: str, path: str):
    """Lit un fichier JSON tel qu'il était dans un commit."""
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def est_salle_valide(salle) -> bool:
    """Détermine si une salle historique est exploitable."""
    if salle is None:
        return False

    salle = str(salle).strip()

    return salle not in ("", "0", "0.0", "None", "null")


def reparer_fichier(path: str) -> int:
    fichier = Path(path)

    if not fichier.exists():
        print(f"\n❌ {path} : fichier introuvable")
        return 0

    # JSON actuel
    try:
        matches_actuels = json.loads(
            fichier.read_text(encoding="utf-8")
        )
    except Exception as e:
        print(f"\n❌ {path} : impossible de lire le JSON : {e}")
        return 0

    # On cible uniquement :
    # - les matchs déjà joués (score non vide)
    # - dont la salle vaut actuellement 0
    a_reparer = {
        m["code"]: m
        for m in matches_actuels
        if m.get("score")
        and str(m.get("salle", "")).strip() in ("0", "0.0")
    }

    if not a_reparer:
        print(f"\n✓ {path} : aucune salle à réparer.")
        return 0

    print(
        f"\n🔎 {path} : {len(a_reparer)} match(s) à réparer."
    )

    commits = git_commits_fichier(path)

    if not commits:
        print(f"❌ Aucun historique Git trouvé pour {path}")
        return 0

    reparations = 0

    # Pour chaque match, on remonte l'historique jusqu'à trouver
    # une version où la salle était correcte.
    for code, match_actuel in a_reparer.items():

        salle_trouvee = None
        commit_trouve = None

        for commit in commits:
            anciens_matches = git_lire_fichier(commit, path)

            if not anciens_matches:
                continue

            ancien = next(
                (
                    m
                    for m in anciens_matches
                    if m.get("code") == code
                ),
                None,
            )

            if not ancien:
                continue

            salle = ancien.get("salle")

            if est_salle_valide(salle):
                salle_trouvee = str(salle).strip()
                commit_trouve = commit
                break

        if salle_trouvee:
            print(
                f"  ✓ Match {code} : "
                f"salle 0 → {salle_trouvee} "
                f"(commit {commit_trouve[:8]})"
            )

            match_actuel["salle"] = salle_trouvee
            reparations += 1

        else:
            print(
                f"  ⚠ Match {code} : "
                f"aucune ancienne salle trouvée"
            )

    # Sauvegarde uniquement si quelque chose a été réparé
    if reparations:
        fichier.write_text(
            json.dumps(
                matches_actuels,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    print(
        f"→ {reparations}/{len(a_reparer)} "
        f"match(s) réparé(s)."
    )

    return reparations


if __name__ == "__main__":
    total = 0

    for fichier in FICHIERS:
        total += reparer_fichier(fichier)

    print(f"\n🏐 Total : {total} salle(s) restaurée(s).")
