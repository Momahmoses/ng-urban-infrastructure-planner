[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=Momahmoses%2Fng-urban-infrastructure-planner&branch=main&mainModule=app.py)

# 🏙 Nigeria Smart Urban Infrastructure Planner

Data-driven urban planning platform for Nigeria's 15 major cities, mapping informal settlements, scoring infrastructure gaps, and prioritizing investment projects using **GIS**, **PySpark K-Means**, **Azure Digital Twins**, and **Streamlit**.

## Problem Statement
70+ million Nigerians live in informal settlements lacking paved roads, piped water, electricity, and sanitation. Lagos alone has 200+ slum communities. This platform helps MHUD, World Bank urban teams, and state governments prioritize infrastructure investment by ROI and gap severity.

## Tech Stack
| Layer | Technology |
|---|---|
| Geospatial | GeoPandas, Folium, Azure Maps |
| Big Data | PySpark K-Means on Azure Databricks |
| Cloud | Azure Blob, Azure Digital Twins, Azure Cognitive Services |
| Dashboard | Streamlit + Plotly |

## Quick Start
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dashboard Features
- Settlement heatmap by infrastructure gap + project overlays
- Gap score bar chart per city
- Access coverage by settlement type (water, electricity, sanitation)
- Projects by type and construction status
- City livability vs infrastructure scatter
- Project ROI prioritization table

## Data Sources (Production)
- **NPC** — National Population Commission settlement data
- **MHUD** — Ministry of Housing & Urban Development
- **World Bank City Resilience** — Urban vulnerability indicators
- **OpenStreetMap** — Building footprints, road network
- **NLMA** — Nigerian Land Mass Administration
