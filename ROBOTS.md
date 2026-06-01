# ROBOTS.txt Analysis — electrogrup.applytojob.com

## Robots.txt

Sursa: `https://electrogrup.applytojob.com/robots.txt`

```
User-agent: *
Disallow: /
```

## Analysis

- **Restrictiv complet**: `/` este complet desalowat pentru toți user-agent-ii
- Scraperul `job_seeker_ro_spider` accesează doar pagina principală de listing (`/apply/jobs/`)
- Se adaugă delay de 1s între request-uri
- Se folosește User-Agent: `job_seeker_ro_spider`
