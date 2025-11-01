<p align="center">
  <a href="README.md">🏠 Forside</a> |
  <a href="README.GamMa.md">📊 GamMa</a> 
</p>


# GamMa – Data & Rapportering

GamMa-projektet er et selvstændigt data- og rapporteringssetup under **data-projects**-samlingen.  
Formålet er at automatisere behandling af medlems- og betalingsdata, skabe grundlag for rapportering, og sikre en genbrugelig dataplatform for GamMa-foreningen.

---

## 🎯 Formål

- Indsamle og transformere data fra bank, MobilePay og medlemsregistre.  
- Etablere en ensartet datamodel i PostgreSQL til analyse og Power BI.  
- Automatisere daglige ETL-processer via Docker-services.  
- Sikre nem eksport (CSV) til deling og backup.  
- Understøtte fremtidig rapportering, fx økonomiske nøgletal og medlemsudvikling.

---

## 🧱 Projektstruktur

```
/data-projects
│
├── /docs/gamma                → Dokumentation, modeller og procesnoter
├── /res/gamma                 → Ressourcer, datafiler og output (fx CSV-eksporter)
├── /src/code/libraries        → Fælles Python-biblioteker (classes, utils, runners)
│
├── /src/code/runtime_definitions/gamma
│   └── Konfigurationsfiler (JSON) der definerer jobs og queries
│
├── /src/code/services/gamma
│   ├── /etl/service_client_to_csv  → Docker-service der eksporterer data til CSV
│   ├── /etl/service_client_to_client
│   └── ... (flere services kan tilføjes)
│
└── /src/workspace-serve/gamma
    └── Power BI-arbejdsfiler og dashboards
```

---

## ⚙️ Teknologi

| Komponent | Formål |
|------------|--------|
| **Python (pandas, SQLAlchemy)** | ETL, data-forberedelse og eksport |
| **PostgreSQL** | Primær database (kører som container) |
| **Docker / Docker Compose** | Kørsel og orkestrering af services |
| **Power BI / Tabular Editor** | Rapportering og semantisk modellering |
| **.env-filer** | Miljøvariabler til database- og servicekonfiguration |
| **CSV-eksporter** | Backup og manuel upload af datakopier |

---

## 🚀 Kom i gang

1. Navigér til projektets service-mappe:
   ```bash
   cd src/code/services/gamma/etl/service_client_to_csv
   ```

2. Start containeren:
   ```bash
   docker compose up --build
   ```

3. Servicen henter data, genererer CSV-filer og gemmer dem i:
   ```
   /backup/
   ```
   (mappes automatisk til `service_client_to_csv/backup/` på din host-maskine)

4. De genererede CSV-filer kan herefter uploades manuelt til fx Google Drive som backup.

---

## 🧩 Projektets logik (kort fortalt)

- **Dataimport:** Henter data fra PostgreSQL og/eller eksterne kilder.  
- **Transformation:** Kombinerer transaktioner, medlemsoplysninger og betalinger.  
- **Eksport:** Gemmer færdige datasæt som CSV i backup-mappen.  
- **Rapportering:** Power BI-dashboard anvender disse datasæt til analyse.

---

## 🧰 Udviklingsprincipper

- Fælles kode genbruges fra `src/code/libraries`.  
- Alle services følger samme Docker-struktur og `.env`-konvention.  
- Konfigurationer gemmes i `runtime_definitions/gamma` og styres via JSON.  
- Al output (fx CSV, logs, modeller) gemmes i `res/gamma` eller `backup`.  

---

## 📄 Licens
Dette projekt er en del af **data-projects**-samlingen og er forbeholdt  
**Abrahim Borgi**. Ingen offentlig distribution uden tilladelse.

---

## 📬 Kontakt
For spørgsmål, kommentarer eller samarbejde:  
**Abrahim Borgi**  
📧 Kontakt via GitHub-profil eller e-mail.