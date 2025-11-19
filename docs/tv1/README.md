# TV ONE -- Simulering, Data & Rapportering

TV ONE-projektet er et selvstændigt data- og rapporteringssetup under
**data-projects**-samlingen.\
Formålet er at simulere streaming- og brugeradfærd, opbygge en datamodel
i PostgreSQL, og levere rapportering via Power BI og Tabular Editor.

![TV ONE -- Simuleringsoversigt](/res/tv1/pbi/OVERVIEW-Page.png)

------------------------------------------------------------------------

## 🎯 Formål

-   Simulere realistiske data for brugere, sessioner og seeradfærd.\
-   Opbygge et fleksibelt ETL-setup med Docker-services.\
-   Etablere en PostgreSQL-datamodel med fokus på KPI'er som *Sessions*,
    *Minutter set*, og *Aktive brugere*.\
-   Udvikle semantisk model og rapportering i Power BI via Tabular
    Editor.\
-   Sikre genbrugelig struktur for fremtidige DR- eller TV-projekter.

------------------------------------------------------------------------

## 🧱 Projektstruktur

    /data-projects
    │
    ├── /docs/drtv-case              → Dokumentation, noter og koncepter
    ├── /res/drtv-case               → Billeder, mockups og testdata
    │
    ├── /src/code/libraries          → Fælles Python-biblioteker (DatabaseClient, utils, simulations)
    │
    ├── /src/code/runtime_definitions/tv1
    │   └── JSON-filer med definitioner for simuleringer og tabeller
    │
    ├── /src/code/service/tv1
    │   ├── /dbt                                 → Opbygger stage og mart 
    │   └── /etl
    │       ├── /service_simulations             → Genererer simulerede data
    │       ├── /etl/service_streaming_sessions  → Opretter sessionsdata og logs
    │       └── ... (flere services kan tilføjes)
    │
    └── /src/workspace-serve/tv1
        ├── /Tabular       → Power BI semantisk model og DAX-measures
        └── /SemanticModel → TMDL-modeller, visuals og metadata

------------------------------------------------------------------------

## ⚙️ Teknologi
| Komponent | Formål |
| --------------------------------- | ----------------------------------------- |
|  **Python (pandas, SQLAlchemy)** |  Data-generering og ETL-pipelines          |
|  **PostgreSQL**                  |  Primær database for simulerede data       |
|  **DBT**                         |  Opbygning af Staging og Marts som bruges i semantisk model |
|  **Docker / Docker Compose**     |  Kørsel og orkestrering af services        |
|  **Tabular Editor 2**            |  Oprettelse af KPI-measures og parametre   |
|  **Power BI Desktop**            |  Visualisering og analyse af resultater    |
|  **.env-filer**                  |  Miljøvariabler til database og services   |

------------------------------------------------------------------------

## 🚀 Kom i gang

1.  Start PostgreSQL og nødvendige services via Docker Compose:

    ``` bash
    docker compose up --build
    ```

2.  Kør Python-simulationen:

    ``` bash
    python src/code/service/tv1/etl/service_simulations/main.py
    ```

3.  De simulerede data gemmes i PostgreSQL og kan herefter anvendes i
    rapporteringen.

4.  Opdater Tabular-modellen:

    ``` bash
    "C:\Program Files (x86)\Tabular Editor\TabularEditor.exe" 
    ".\src\workspace-serve\tv1\SemanticModel\TV1 SemanticModel.SemanticModel\definition\model.tmdl" 
    -S ".\src\workspace-serve\tv1\Tabular\Measures\KPI\KPI_MEASURES.csx" -D
    ```

------------------------------------------------------------------------

## 🧩 Projektets logik (kort fortalt)

-   **Simulering:** Genererer brugere, sessioner og afspilninger ud fra
    realistiske mønstre.\
-   **ETL:** Skriver data til PostgreSQL, dbt med runtime-definitioner for
    struktur.\
-   **Rapportering:** Power BI benytter den semantiske model med KPI'er
    som *Sessions*, *Minutter set* og *Aktive brugere*.\
-   **Automatisering:** Docker-services kan afvikle hele dataflowet fra
    simulering til rapportering.

------------------------------------------------------------------------

## 🧰 Udviklingsprincipper

-   Alle services følger samme struktur og miljøopsætning som øvrige
    projekter.\
-   Tabular Editor scripts (`.csx`) anvendes til at oprette KPI'er og
    parametre dynamisk.\
-   Konfigurationer (runtime vars) gemmes i `runtime_definitions/tv1/`.\
-   Genbrug af fælles kode fra `libraries/`.

------------------------------------------------------------------------

## 📄 Licens

Dette projekt er en del af **data-projects**-samlingen og er forbeholdt\
**Abrahim Borgi**. Ingen offentlig distribution uden tilladelse.

------------------------------------------------------------------------

## 📬 Kontakt

For spørgsmål, kommentarer eller samarbejde:\
**Abrahim Borgi**\
📧 Kontakt via GitHub-profil eller e-mail.