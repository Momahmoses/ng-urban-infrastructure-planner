"""GIS: Settlement mapping, infrastructure gap visualization, project overlay."""
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import HeatMap, MarkerCluster
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.generate_data import generate_settlements, generate_infrastructure_projects


SETTLEMENT_COLORS = {
    "Formal": "#388e3c", "Informal/Slum": "#d32f2f",
    "Peri-urban": "#f57c00", "Industrial": "#1565c0", "Mixed-use": "#7b1fa2"
}

STATUS_COLORS = {
    "Completed": "green", "Under Construction": "blue",
    "Planned": "orange", "Stalled": "red"
}


def build_urban_map(settlements_df: pd.DataFrame,
                    projects_df: pd.DataFrame) -> folium.Map:
    m = folium.Map(location=[9.08, 8.67], zoom_start=6, tiles="CartoDB positron")

    heat = [[r.lat, r.lon, r.infrastructure_gap_score]
            for _, r in settlements_df.iterrows()]
    HeatMap(heat, radius=14, blur=12, min_opacity=0.3,
            gradient={"0.3": "green", "0.5": "yellow", "0.8": "red"}).add_to(m)

    cluster = MarkerCluster(name="Settlements").add_to(m)
    for _, row in settlements_df.sample(min(300, len(settlements_df)), random_state=42).iterrows():
        color = SETTLEMENT_COLORS.get(row["settlement_type"], "gray")
        folium.CircleMarker(
            location=[row.lat, row.lon], radius=5,
            color=color, fill=True, fill_opacity=0.75,
            popup=(f"<b>{row['city']}</b> — {row['settlement_type']}<br>"
                   f"Pop: {row['population']:,}<br>"
                   f"Water: {row['water_access_pct']}%<br>"
                   f"Electricity: {row['electricity_access_pct']}%<br>"
                   f"Gap Score: {row['infrastructure_gap_score']:.2f}"),
        ).add_to(cluster)

    for _, proj in projects_df.iterrows():
        color = STATUS_COLORS.get(proj["status"], "gray")
        folium.Marker(
            location=[proj.lat, proj.lon],
            popup=(f"<b>{proj['type']}</b><br>{proj['city']}<br>"
                   f"Status: {proj['status']}<br>"
                   f"Budget: ₦{proj['budget_ngn_million']:,.0f}M<br>"
                   f"Beneficiaries: {proj['population_benefiting']:,}"),
            icon=folium.Icon(color=color, icon="building", prefix="fa"),
        ).add_to(m)

    folium.LayerControl().add_to(m)
    return m


if __name__ == "__main__":
    settlements = generate_settlements(300)
    projects = generate_infrastructure_projects()
    m = build_urban_map(settlements, projects)
    os.makedirs("app", exist_ok=True)
    m.save("app/urban_map.html")
    print("Map saved.")
