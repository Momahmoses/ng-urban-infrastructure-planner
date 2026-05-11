"""Azure config for Urban Infrastructure Planner."""
import os

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
AZURE_DIGITAL_TWINS_ENDPOINT = os.getenv("AZURE_DIGITAL_TWINS_ENDPOINT", "")
AZURE_MAPS_KEY = os.getenv("AZURE_MAPS_KEY", "")
AZURE_COGNITIVE_SERVICES_KEY = os.getenv("AZURE_COGNITIVE_SERVICES_KEY", "")
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST", "")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "")


def get_digital_twins_config() -> dict:
    return {
        "endpoint": AZURE_DIGITAL_TWINS_ENDPOINT,
        "models": ["Settlement", "Infrastructure", "Road", "UtilityGrid"],
        "note": "Azure Digital Twins models settlements and infrastructure as live digital replicas",
    }
