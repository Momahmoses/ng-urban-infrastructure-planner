import pandas as pd
import numpy as np
import os

URBAN_AREAS = [
    ("Lagos", 6.5244, 3.3792, 15388000, "Megacity"),
    ("Kano", 12.0022, 8.5920, 4103000, "Metropolis"),
    ("Ibadan", 7.3775, 3.9470, 3565000, "Metropolis"),
    ("Abuja", 9.0765, 7.3986, 3121000, "Capital"),
    ("Port Harcourt", 4.8156, 7.0498, 1866000, "Metropolis"),
    ("Kaduna", 10.5222, 7.4383, 1133000, "Major City"),
    ("Benin City", 6.3350, 5.6037, 1147000, "Major City"),
    ("Maiduguri", 11.8320, 13.1520, 803000, "Major City"),
    ("Enugu", 6.4584, 7.5464, 722000, "Major City"),
    ("Warri", 5.5167, 5.7333, 604000, "Major City"),
    ("Onitsha", 6.1667, 6.7833, 561000, "Major City"),
    ("Sokoto", 13.0059, 5.2476, 480000, "Secondary City"),
    ("Jos", 9.9285, 8.8921, 817000, "Major City"),
    ("Aba", 5.1060, 7.3670, 897000, "Major City"),
    ("Ilorin", 8.4966, 4.5426, 847000, "Major City"),
]

INFRASTRUCTURE_TYPES = ["Road", "School", "Healthcare", "Water Supply",
                          "Electricity", "Market", "Public Transport", "Sewage"]

SETTLEMENT_TYPES = ["Formal", "Informal/Slum", "Peri-urban", "Industrial", "Mixed-use"]


def generate_settlements(n: int = 800) -> pd.DataFrame:
    np.random.seed(42)
    records = []
    for i in range(n):
        city_info = URBAN_AREAS[np.random.randint(len(URBAN_AREAS))]
        city, clat, clon, pop, city_type = city_info
        settlement_type = np.random.choice(SETTLEMENT_TYPES, p=[0.30, 0.35, 0.20, 0.08, 0.07])
        is_informal = settlement_type == "Informal/Slum"
        records.append({
            "settlement_id": f"STL-{i+1:05d}",
            "city": city, "city_type": city_type,
            "lat": clat + np.random.uniform(-0.15, 0.15),
            "lon": clon + np.random.uniform(-0.15, 0.15),
            "settlement_type": settlement_type,
            "population": int(np.random.exponential(8000)),
            "area_km2": round(np.random.uniform(0.1, 5.0), 2),
            "housing_density": round(np.random.uniform(50, 800), 0),
            "has_paved_road": not is_informal or np.random.random() > 0.7,
            "road_quality": np.random.choice(["Good", "Fair", "Poor"],
                            p=[0.2, 0.3, 0.5] if is_informal else [0.4, 0.4, 0.2]),
            "schools_count": int(np.random.poisson(1.5)),
            "health_facilities": int(np.random.poisson(0.8)),
            "water_access_pct": round(np.random.uniform(15, 95), 1),
            "electricity_access_pct": round(np.random.uniform(20, 98), 1),
            "sanitation_access_pct": round(np.random.uniform(10, 90), 1),
            "avg_income_monthly_ngn": int(np.random.uniform(20000, 500000)),
            "flood_risk": np.random.choice(["Low", "Moderate", "High"], p=[0.4, 0.35, 0.25]),
            "infrastructure_gap_score": round(np.random.uniform(0.2, 0.95)
                                              if is_informal else np.random.uniform(0.05, 0.6), 3),
        })
    return pd.DataFrame(records)


def generate_infrastructure_projects() -> pd.DataFrame:
    np.random.seed(42)
    records = []
    for i in range(150):
        city_info = URBAN_AREAS[np.random.randint(len(URBAN_AREAS))]
        city, clat, clon, pop, city_type = city_info
        infra_type = np.random.choice(INFRASTRUCTURE_TYPES)
        records.append({
            "project_id": f"PROJ-{i+1:04d}",
            "city": city,
            "lat": clat + np.random.uniform(-0.12, 0.12),
            "lon": clon + np.random.uniform(-0.12, 0.12),
            "type": infra_type,
            "status": np.random.choice(["Planned", "Under Construction", "Completed", "Stalled"],
                      p=[0.30, 0.25, 0.30, 0.15]),
            "budget_ngn_million": round(np.random.exponential(500), 0),
            "population_benefiting": int(np.random.exponential(20000)),
            "completion_year": int(np.random.randint(2023, 2028)),
            "priority_score": round(np.random.uniform(0.2, 1.0), 3),
        })
    return pd.DataFrame(records)


def generate_city_scores() -> pd.DataFrame:
    np.random.seed(42)
    return pd.DataFrame([
        {"city": city, "city_type": ctype, "lat": clat, "lon": clon, "population": pop,
         "livability_score": round(np.random.uniform(0.2, 0.85), 3),
         "infrastructure_index": round(np.random.uniform(0.15, 0.80), 3),
         "urban_density_pop_km2": round(pop / np.random.uniform(100, 1500), 0),
         "informal_settlement_pct": round(np.random.uniform(20, 65), 1),
         "annual_pop_growth_pct": round(np.random.uniform(2.5, 6.5), 2),
        }
        for city, clat, clon, pop, ctype in URBAN_AREAS
    ])


def save_all(output_dir: str = "data"):
    os.makedirs(output_dir, exist_ok=True)
    generate_settlements().to_csv(f"{output_dir}/settlements.csv", index=False)
    generate_infrastructure_projects().to_csv(f"{output_dir}/projects.csv", index=False)
    generate_city_scores().to_csv(f"{output_dir}/city_scores.csv", index=False)
    print("Urban data generated.")


if __name__ == "__main__":
    save_all()
