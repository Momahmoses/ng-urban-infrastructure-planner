"""Urban Infrastructure PySpark Pipeline — Azure Databricks."""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
import os


def get_spark():
    return SparkSession.builder.appName("UrbanInfrastructurePipeline").getOrCreate()


def compute_settlement_gap_scores(settlements_df):
    """Compute composite infrastructure gap score per settlement."""
    return (
        settlements_df
        .withColumn(
            "computed_gap",
            (1 - F.col("water_access_pct") / 100) * 0.25 +
            (1 - F.col("electricity_access_pct") / 100) * 0.25 +
            (1 - F.col("sanitation_access_pct") / 100) * 0.25 +
            F.when(F.col("has_paved_road") == False, 0.25).otherwise(0.0)
        )
        .withColumn(
            "intervention_priority",
            F.when(F.col("computed_gap") >= 0.65, "Critical")
             .when(F.col("computed_gap") >= 0.45, "High")
             .when(F.col("computed_gap") >= 0.25, "Medium")
             .otherwise("Low")
        )
    )


def cluster_settlements(settlements_df):
    """K-Means clustering to group settlements by infrastructure profile."""
    assembler = VectorAssembler(
        inputCols=["water_access_pct", "electricity_access_pct",
                   "sanitation_access_pct", "housing_density"],
        outputCol="features"
    )
    df_vec = assembler.transform(settlements_df.fillna(0))
    kmeans = KMeans(featuresCol="features", k=4, seed=42)
    model = kmeans.fit(df_vec)
    return model.transform(df_vec)


def prioritize_projects(projects_df):
    return (
        projects_df
        .withColumn("roi_score",
                    F.col("population_benefiting") / (F.col("budget_ngn_million") + 1))
        .orderBy(F.col("roi_score").desc(), F.col("priority_score").desc())
    )


if __name__ == "__main__":
    spark = get_spark()
    settlements = spark.read.csv("data/settlements.csv", header=True, inferSchema=True)
    projects = spark.read.csv("data/projects.csv", header=True, inferSchema=True)
    gap_df = compute_settlement_gap_scores(settlements)
    gap_df.show(10)
    clustered = cluster_settlements(settlements)
    clustered.groupBy("prediction").count().show()
    roi_df = prioritize_projects(projects)
    roi_df.show(10)
    spark.stop()
