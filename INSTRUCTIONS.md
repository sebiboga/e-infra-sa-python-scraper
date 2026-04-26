# Project Instructions & Knowledge Base

This document summarizes the technical stack, configurations, and critical rules established for this project.

## 🛠 Technology Stack
- **Languages**: Python
- **Libraries**: `pysolr`, `requests`, `python-dotenv`, `pytest`
- **Data Sources**:
    - **MCP demoanaf**: For fetching official Romanian company details (CUI, legal name, address, etc.).
    - **Solr**: The target backend for storing job and company data.

## 🔍 Solr Configuration
- **Base URL**: `https://solr.peviitor.ro/solr`
- **Authentication**: Basic Auth (credentials stored in `.env.local`).
- **Cores**:
    - `job`: Stores job listings.
    - `company`: Stores company metadata.

### Unique Keys
- **`job` core**: Unique key is **`url`**.
- **`company` core**: Unique key is **`id`**.

## ⚠️ Critical Rule: No Partial Updates
**DO NOT use atomic or partial updates in Solr.**
- Partial updates cause data loss in the current environment.
- **Requirement**: Always fetch the **entire** existing document, merge the new data, and re-push the **full** document to Solr.
- Use the `safe_update` function in `solr_connection.py` to handle this automatically.

## 📋 Data Models
Refer to [readme.md](readme.md) for the detailed schema of the `job` and `company` models.

### Job Model Fields
`url`, `title`, `company`, `cif`, `location`, `tags`, `workmode`, `date`, `status`, `vdate`, `expirationdate`, `salary`.
- **`date`**: Must be added dynamically in UTC ISO8601 format (ex: "2026-04-26T10:00:00Z").
- **`cif`**: Must be explicitly mapped and included for each job's company to avoid collisions.

### Company Model Fields
`id` (CUI), `company`, `brand`, `group`, `status`, `location`, `website`, `career`, `lastScraped`, `scraperFile`.

## 🧪 Testing
- Integration tests are located in `tests/test_solr_integration.py`.
- Run tests with: `export PYTHONPATH=$PYTHONPATH:. && python3 tests/test_solr_integration.py`.
- Ensure `.env.local` is correctly configured before running.
