# E-INFRA S.A. Python Scraper

Acest proiect conține un scraper web pentru grupul E-INFRA (Electrogrup, Direct One, Netcity, Nova Power & Gas, WESEE).

## Configurare
Proiectul folosește GitHub Actions pentru a rula zilnic. Credențialele pentru Solr trebuie configurate în secțiunea **Secrets** a repozitoriului:
- `SOLR_USER`
- `SOLR_PASS`
- `SOLR_JOBS_CORE`
- `SOLR_COMPANY_CORE`

## Structură
- `einfra_group_scraper.py`: Scriptul principal de scraping.
- `solr_connection.py`: Utilitar pentru conexiunea cu Solr.
- `.github/workflows/scraper.yml`: Configurația pentru rulare automată.
- `OPEN_SOURCE.md`: Ghidul de standarde pentru repozitoare publice.

## Standarde Proiect
Acest repozitoriu respectă standardele definite în [OPEN_SOURCE.md](OPEN_SOURCE.md).
