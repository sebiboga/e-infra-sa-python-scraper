# Open Source Standards for Scraper Projects

Acest document definește setul minim de fișiere și standarde necesare pentru ca un repozitoriu de scraping să fie considerat pregătit pentru publicul larg (Open Source).

## 📂 Fișiere Obligatorii

### 1. `README.md`
- **Scop**: Prezentarea proiectului, instrucțiuni de instalare și utilizare.
- **Conținut**: Descriere, stack tehnic, configurare mediu, exemple de rulare.

### 2. `LICENSE`
- **Scop**: Definește condițiile legale sub care codul poate fi utilizat, modificat sau distribuit.
- **Standard**: De regulă, folosim **MIT License** pentru proiectele de scraping.

### 3. `CONTRIBUTING.md`
- **Scop**: Oferă ghidaj persoanelor care doresc să contribuie la proiect.
- **Conținut**: Workflow-ul de Git (fork, branch, PR), standarde de cod, configurarea mediului de dezvoltare.

### 4. `CHANGELOG.md`
- **Scop**: Urmărirea evoluției proiectului în timp.
- **Standard**: Bazat pe [Keep a Changelog](https://keepachangelog.com/). Include secțiuni pentru `Added`, `Changed`, `Fixed`, `Removed`.

### 5. `SECURITY.md`
- **Scop**: Definește modul în care trebuie raportate vulnerabilitățile fără a le face publice imediat.
- **Regulă critică**: Include avertismente despre NU commite fișiere `.env` sau credențiale.

### 6. `.gitignore`
- **Scop**: Prevenirea încărcării fișierelor inutile sau sensibile.
- **Ce excludem**: `venv/`, `.env`, `.env.local`, `__pycache__/`, `.DS_Store`, setări de IDE.

### 7. `.github/workflows/`
- **Scop**: Automatizarea proceselor de scraping și testare (CI/CD).
- **Fișier**: `scraper.yml` pentru rulări programate (Cron) și validări automate.

---

## 🔐 Gestionarea Secretelor (Critical)
NICIODATĂ nu se includ parole, token-uri sau chei API în codul sursă.
1. Folosește `python-dotenv` sau `dotenv` (Node) pentru a citi din `.env.local`.
2. Adaugă `.env.local` în `.gitignore`.
3. Configurează aceleași chei în **GitHub Secrets**.
4. Formează fișierul `.env.local` dinamic în workflow-ul de GitHub Actions.
