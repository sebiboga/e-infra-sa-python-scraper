# E-INFRA S.A. Python Scraper

[![Scraper Run](https://github.com/sebiboga/e-infra-sa-python-scraper/actions/workflows/scraper.yml/badge.svg)](https://github.com/sebiboga/e-infra-sa-python-scraper/actions/workflows/scraper.yml)
[![Tests](https://github.com/sebiboga/e-infra-sa-python-scraper/actions/workflows/tests.yml/badge.svg)](https://github.com/sebiboga/e-infra-sa-python-scraper/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

**Scraper:** `job_seeker_ro_spider`

Acest proiect conține un scraper web pentru grupul E-INFRA (Electrogrup, Direct One, Netcity, Nova Power & Gas, WESEE) care publică job-uri în platforma [peviitor.ro](https://peviitor.ro).

## Companii

| Company | CIF | Status |
|---------|:---:|:------:|
| E-INFRA S.A. | 38647188 | activ |
| ELECTROGRUP SA | 9256208 | activ |
| NOVA POWER & GAS S.A. | 18680651 | activ |
| NETCITY TELECOM S.A. | 22902080 | activ |
| DIRECT ONE SA | 22913844 | activ |
| WIND ENERGY SERVICE EAST EUROPE SRL | 26669972 | activ |

## Configurare

Proiectul folosește GitHub Actions pentru a rula zilnic. Credențialele pentru Solr trebuie configurate în secțiunea **Secrets** a repozitoriului:
- `SOLR_USER`
- `SOLR_PASS`

## Structură

- `einfra_group_scraper.py`: Scriptul principal de scraping (User-Agent: `job_seeker_ro_spider`).
- `solr_connection.py`: Utilitar pentru conexiunea cu Solr.
- `tests/validate_einfra_jobs.py`: Validare și ștergere job-uri expirate.
- `.github/workflows/scraper.yml`: Rulare automată zilnică (8 AM).
- `.github/workflows/tests.yml`: Testare și validare job-uri.
- `payloads/`: JSON-uri pentru core-ul company în Solr.
- `docs/index.html`: Pagină GitHub Pages cu statusul job-urilor.
- `OPEN_SOURCE.md`: Ghidul de standarde pentru repozitoare publice.

## ROBOTS.txt Policy

Scraperul `job_seeker_ro_spider` respectă regulile din `robots.txt`:
- Se accesează doar pagina de listing (`/apply/jobs/`)
- Se adaugă delay de 0.5s între request-uri
- User-Agent: `job_seeker_ro_spider`

## Dezvoltare

```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper manually
python einfra_group_scraper.py

# Run tests (skip SOLR)
python -m pytest tests/ -m "not solr"

# Run all tests (SOLR credentials required)
python -m pytest tests/
```

## Disclaimer

Acest proiect nu are nicio afiliere cu E-INFRA S.A. sau companiile din grup. Datele sunt colectate doar din surse publice.

## Acknowledgments

Proiect dezvoltat pentru [peviitor.ro](https://peviitor.ro) — platforma care centralizează ofertele de muncă din România.
