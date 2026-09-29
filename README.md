# 🏐 VOLLEY

Calendriers automatiques des matchs de l'équipe de volley, mis à jour chaque jour à partir du site de la FFVB.

## S'abonner aux calendriers

Copie l'URL de ton équipe :

| Équipe | URL |
|---|---|
| SM-DEP | `https://raw.githubusercontent.com/Charlyy95/VOLLEY/main/calendrier_SM-DEP.ics` |
| SF-TAV | `https://raw.githubusercontent.com/Charlyy95/VOLLEY/main/calendrier_SF-TAV.ics` |
| SF-DEP | `https://raw.githubusercontent.com/Charlyy95/VOLLEY/main/calendrier_SF-DEP.ics` |

**iPhone / iPad** :  Calendrier > Nouv. calendrier > Ajouter un calendrier avec abonnement, puis colle l'URL.

**Mac** : Calendrier > Fichier > Nouvel abonnement à un calendrier, puis colle l'URL.

**Google Agenda** : Autres agendas (+) > À partir de l'URL, puis colle l'URL.

Le calendrier se rafraîchit tout seul. Sur iPhone, cela peut prendre quelques heures après une mise à jour.

## Comment ça marche

1. Tous les jours vers 3h47 UTC, un workflow GitHub Actions lance `scraper.py`.
2. Le scraper récupère le calendrier complet de chaque équipe sur [ffvbbeach.org](https://www.ffvbbeach.org).
3. Il ignore les journées de repos (`xxxxx`) et génère un fichier `matches_*.json` et un fichier `calendrier_*.ics` par équipe.
4. Si les fichiers ont changé, le workflow les commit automatiquement.

## Fichiers

- `scraper.py` : récupération des matchs et génération des fichiers
- `.github/workflows/scrape-quotidien.yml` : planification quotidienne
- `matches_*.json` : données brutes des matchs
- `calendrier_*.ics` : calendriers à importer

## Lancer le scraper à la main

```bash
pip install requests beautifulsoup4
python scraper.py
```

Ou depuis l'onglet **Actions** du dépôt, en cliquant sur **Run workflow**.

## Ajouter ou changer une équipe

Modifie la liste `EQUIPES` dans `scraper.py` (saison, poule et numéro d'équipe).

## Alerte en cas de problème

Si le site FFVB est en panne ou si une équipe a 0 match, le workflow échoue et GitHub envoie un e-mail. Les anciens fichiers sont conservés.
