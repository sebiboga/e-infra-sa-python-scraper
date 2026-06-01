# AGENTS.md — Rules for AI agents

## Project
E-INFRA S.A. group scraper for peviitor.ro (Python, requests, BeautifulSoup)

## Critical Rules

### 1. Temporary Files
All temporary/scratch files MUST go in `tmp/` inside the project root.
NEVER use paths outside the project (e.g. `C:\Users\...\AppData\Local\Temp\opencode`).

### 2. Issues & GitHub
- **Orice modificare de cod trebuie să aibă un issue în GitHub Issues** (vezi [ISSUES.md](ISSUES.md))
- Excepții: typo-uri, whitespace, documentație minoră
- Create a GitHub issue before implementing any change
- Commit messages must reference the issue they close
- Never commit credentials (`.env.local`, `*.pem`, etc.)
- Push after commit

### 3. Environment Variables
- `SOLR_USER=your-solr-user` and `SOLR_PASS=your-solr-password` must be set in `.env.local` for SOLR tests
- `.env.local` is in `.gitignore` — never commit it

### 4. Testing
```bash
# Unit tests (no env vars needed)
python -m pytest tests/ -m "not solr"

# Integration tests (SOLR conditional)
python -m pytest tests/ -m solr
```

### 5. conftest.py
- A `conftest.py` at project root defines a `solr` pytest marker with `addoption`
- SOLR tests use `@pytest.mark.solr` — auto-skip when `SOLR_USER` or `SOLR_PASS` not set via `pytest_collection_modifyitems`

### 6. Module Structure
- `einfra_group_scraper.py` — main scraper (electrogrup.applytojob.com)
- `solr_connection.py` — SOLR connection utility (pysolr)
- `tests/` — test suite
- `payloads/` — company JSON payloads for SOLR company core
