"""Nigeria Smart Urban Infrastructure Planner — Streamlit Dashboard"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from data.generate_data import (generate_settlements, generate_infrastructure_projects,
                                  generate_city_scores, INFRASTRUCTURE_TYPES, SETTLEMENT_TYPES)
from gis.spatial_analysis import build_urban_map

st.set_page_config(page_title="NG Urban Planner", page_icon="🏙", layout="wide")
st.markdown("""<style>
.kpi{background:#1a237e;color:white;padding:14px;border-radius:8px;text-align:center;}
.kpi-val{font-size:1.9rem;font-weight:700;}
.kpi-lbl{font-size:.8rem;opacity:.85;}
</style>""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    settlements = generate_settlements(600)
    projects = generate_infrastructure_projects()
    city_scores = generate_city_scores()
    settlements["gap_computed"] = (
        (1 - settlements["water_access_pct"] / 100) * 0.25 +
        (1 - settlements["electricity_access_pct"] / 100) * 0.25 +
        (1 - settlements["sanitation_access_pct"] / 100) * 0.25 +
        settlements["has_paved_road"].apply(lambda x: 0.0 if x else 0.25)
    )
    return settlements, projects, city_scores


def main():
    settlements_df, projects_df, city_scores_df = load_data()

    with st.sidebar:
        st.title("🏙 Urban Planner")
        st.caption("Nigeria Infrastructure Intelligence")
        st.divider()
        city_filter = st.multiselect("City", settlements_df["city"].unique().tolist(),
                                     default=settlements_df["city"].unique().tolist()[:5])
        settlement_filter = st.multiselect("Settlement Type", SETTLEMENT_TYPES,
                                            default=SETTLEMENT_TYPES)
        project_status = st.multiselect("Project Status",
                                         ["Planned", "Under Construction", "Completed", "Stalled"],
                                         default=["Planned", "Under Construction", "Stalled"])
        gap_threshold = st.slider("Min Gap Score", 0.0, 1.0, 0.0, 0.05)
        st.divider()
        st.markdown("**Azure Services**")
        st.success("Azure Cognitive Services")
        st.info("Azure Databricks")
        st.warning("Azure Maps + Digital Twins")

    stl_filtered = settlements_df[
        settlements_df["city"].isin(city_filter) &
        settlements_df["settlement_type"].isin(settlement_filter) &
        (settlements_df["gap_computed"] >= gap_threshold)
    ]
    proj_filtered = projects_df[
        projects_df["city"].isin(city_filter) &
        projects_df["status"].isin(project_status)
    ]

    st.title("🏙 Nigeria Smart Urban Infrastructure Planner")
    st.caption("Settlement mapping · Gap scoring · Project prioritization · GIS + PySpark + Azure Digital Twins")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    informal = len(stl_filtered[stl_filtered["settlement_type"] == "Informal/Slum"])
    avg_gap = stl_filtered["gap_computed"].mean()
    critical = len(stl_filtered[stl_filtered["gap_computed"] > 0.65])
    total_proj_budget = proj_filtered["budget_ngn_million"].sum()
    for col, val, lbl in zip(
        [c1, c2, c3, c4],
        [f"{informal:,}", f"{avg_gap:.2f}", critical, f"₦{total_proj_budget:,.0f}M"],
        ["Informal Settlements", "Avg Gap Score", "Critical Gap Areas", "Projects Budget"]
    ):
        col.markdown(f'<div class="kpi"><div class="kpi-val">{val}</div>'
                     f'<div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.divider()
    col_map, col_chart = st.columns([3, 2])

    with col_map:
        st.subheader("🗺 Settlement & Infrastructure Map")
        m = build_urban_map(stl_filtered, proj_filtered)
        st_folium(m, width=700, height=460)

    with col_chart:
        st.subheader("📊 Infrastructure Gap by City")
        city_gap = stl_filtered.groupby("city")["gap_computed"].mean().sort_values().reset_index()
        fig = px.bar(city_gap, x="gap_computed", y="city", orientation="h",
                     color="gap_computed", color_continuous_scale="RdYlGn_r",
                     labels={"gap_computed": "Avg Gap Score", "city": ""},
                     height=460)
        fig.update_layout(coloraxis_showscale=False,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=0, r=10, t=5, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    col_access, col_proj = st.columns(2)

    with col_access:
        st.subheader("💡 Access by Settlement Type")
        access_by_type = (stl_filtered.groupby("settlement_type")
                          .agg(water=("water_access_pct", "mean"),
                               electricity=("electricity_access_pct", "mean"),
                               sanitation=("sanitation_access_pct", "mean"))
                          .reset_index())
        fig_a = px.bar(
            access_by_type.melt(id_vars="settlement_type", var_name="Service", value_name="Coverage"),
            x="settlement_type", y="Coverage", color="Service", barmode="group",
            color_discrete_sequence=["#1565c0", "#f57c00", "#388e3c"],
            labels={"settlement_type": "Settlement Type", "Coverage": "Coverage (%)"}
        )
        fig_a.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=0, r=0, t=5, b=0))
        st.plotly_chart(fig_a, use_container_width=True)

    with col_proj:
        st.subheader("🏗 Projects by Type & Status")
        proj_type = proj_filtered.groupby(["type", "status"]).size().reset_index(name="count")
        fig_p = px.bar(proj_type, x="type", y="count", color="status",
                       color_discrete_map={"Completed": "#388e3c", "Under Construction": "#1565c0",
                                           "Planned": "#f57c00", "Stalled": "#d32f2f"},
                       labels={"type": "Infrastructure Type", "count": "Projects", "status": "Status"})
        fig_p.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=0, r=0, t=5, b=0))
        st.plotly_chart(fig_p, use_container_width=True)

    st.divider()
    st.subheader("🏆 City Livability & Infrastructure Ranking")
    fig_city = px.scatter(
        city_scores_df, x="infrastructure_index", y="livability_score",
        size="population", color="city_type", hover_name="city",
        size_max=40,
        labels={"infrastructure_index": "Infrastructure Index",
                "livability_score": "Livability Score", "city_type": "City Type"},
    )
    fig_city.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_city, use_container_width=True)

    st.divider()
    st.subheader("📋 Highest-Priority Projects by ROI")
    proj_priority = proj_filtered.copy()
    proj_priority["roi_score"] = proj_priority["population_benefiting"] / (proj_priority["budget_ngn_million"] + 1)
    st.dataframe(
        proj_priority[["project_id", "city", "type", "status", "budget_ngn_million",
                        "population_benefiting", "roi_score", "completion_year"]]
        .sort_values("roi_score", ascending=False).head(30)
        .style.background_gradient(subset=["roi_score"], cmap="Greens"),
        use_container_width=True, height=300,
    )
    st.caption("Data: Synthetic — replace with NPC, MHUD, World Bank City Resilience, "
               "OpenStreetMap building footprints. Pipeline: Azure Databricks + Azure Digital Twins.")


if __name__ == "__main__":
    main()
