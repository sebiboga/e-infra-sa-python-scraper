# From EPAM

Acest scraper a fost creat după sablonul [epam-systems-international-srl-nodejs-scraper](https://github.com/sebiboga/epam-systems-international-srl-nodejs-scraper).

## Relația cu EPAM

Toate deciziile arhitecturale, configurațiile și îmbunătățirile făcute pe EPAM trebuie aduse și aici.

### Ce se sincronizează

| Componentă | Fișier EPAM | Fișier E-INFRA |
|------------|-------------|-----------------|
| SOLR operations | `solr.js` | `solr_connection.py` |
| Main scraper | `index.js` | `einfra_group_scraper.py` |
| Unit/integration tests | `tests/` | `tests/` |
| GitHub workflows | `.github/workflows/` | `.github/workflows/` |
| Project rules | `AGENTS.md` | *(n/a)* |
| Issues & conventions | `ISSUES.md` | *(n/a)* |
| Repo topics | `TOPICS.md` | *(n/a)* |
| Repo About update | `UPDATE-REPO-ABOUT.md` | *(n/a)* |

### Ce NU se sincronizează

- **Logica de scraping** — EPAM ia joburi dintr-un API JSON, E-INFRA face scraping HTML pe electrogrup.applytojob.com
- **Limbajul** — EPAM e Node.js/ESM, E-INFRA e Python
- **Numele companiei / CIF-urile** — fiecare are propriile CIF-uri și brand-uri
- **Testele specifice** — testele sunt adaptate la sursa de date a fiecărui scraper

## Workflow de portare

1. Se face o modificare pe EPAM (cu issue, branch, PR)
2. Se identifică fișierele corespunzătoare din tabelul de mai sus
3. Se portează modificarea pe E-INFRA
4. Se creează issue și pe E-INFRA
5. Se commit și push

## Motiv

EPAM este scraperul de referință — primul creat, cel mai bine testat, cu cele mai multe îmbunătățiri. E-INFRA păstrează același pattern pentru consistență.
