import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

print(f"Analysis run at: {datetime.now()}")

#  LOAD 
print("Loading dataset...")
df = pd.read_csv("All_Diets.csv")
print(f"Dataset shape: {df.shape}")
print(df.head())

# DATA CLEANING 
print("\n" + "="*50)
print("DATA CLEANING")
print("="*50)

numeric_columns = ["Protein(g)", "Carbs(g)", "Fat(g)"]
print("\nMissing values before cleaning:")
print(df.isnull().sum())

for col in numeric_columns:
    if df[col].isnull().any():
        mean_value = df[col].mean()
        df[col].fillna(mean_value, inplace=True)
        print(f"Filled {col} missing values with mean: {mean_value:.2f}")

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# ANALYSIS 1: Average Macronutrients by Diet Type 
print("\n" + "="*50)
print("ANALYSIS 1: Average Macronutrients by Diet Type")
print("="*50)
avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()
print(avg_macros)

#ANALYSIS 2: Top 5 Protein-Rich Recipes per Diet Type 
print("\n" + "="*50)
print("ANALYSIS 2: Top 5 Protein-Rich Recipes per Diet Type")
print("="*50)
top_protein = (
    df.sort_values("Protein(g)", ascending=False)
    .groupby("Diet_type")
    .head(5)
)
print(top_protein[["Diet_type", "Recipe_name", "Protein(g)"]])

# ANALYSIS 3: Diet Type with Highest Protein 
print("\n" + "="*50)
print("ANALYSIS 3: Diet Type with Highest Protein Content")
print("="*50)
highest_protein_diet = avg_macros["Protein(g)"].idxmax()
highest_protein_value = avg_macros["Protein(g)"].max()
print(f"Highest protein diet: {highest_protein_diet}")
print(f"Average protein: {highest_protein_value:.2f}g")

# ANALYSIS 4: Most Common Cuisines per Diet Type 
print("\n" + "="*50)
print("ANALYSIS 4: Most Common Cuisines per Diet Type")
print("="*50)
most_common_cuisines = df.groupby("Diet_type")["Cuisine_type"].agg(
    lambda x: x.mode()[0] if len(x.mode()) > 0 else "N/A"
)
print(most_common_cuisines)

#  ANALYSIS 5: New Metrics 
print("\n" + "="*50)
print("ANALYSIS 5: Creating New Metrics")
print("="*50)
df["Protein_to_Carbs_ratio"] = df["Protein(g)"] / df["Carbs(g)"].replace(0, np.nan)
df["Carbs_to_Fat_ratio"] = df["Carbs(g)"] / df["Fat(g)"].replace(0, np.nan)
df.to_csv("processed_diets.csv", index=False)
print("Processed data saved to processed_diets.csv")

# VISUALIZATIONS 
print("\n" + "="*50)
print("CREATING VISUALIZATIONS")
print("="*50)

import os
os.makedirs("outputs", exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
ts = datetime.now().strftime('%Y-%m-%d %H:%M')

# VIZ 1 — Bar chart
avg_macros_reset = avg_macros.reset_index()
avg_macros_melted = avg_macros_reset.melt(
    id_vars="Diet_type",
    value_vars=["Protein(g)", "Carbs(g)", "Fat(g)"],
    var_name="Macronutrient",
    value_name="Average (g)",
)
plt.figure()
sns.barplot(data=avg_macros_melted, x="Diet_type", y="Average (g)",
            hue="Macronutrient", palette="Set2")
plt.title(f"Average Macronutrients by Diet Type - {ts}")
plt.xlabel("Diet Type")
plt.ylabel("Average (g)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/bar_macros.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: outputs/bar_macros.png")

# VIZ 2 — Heatmap
plt.figure()
sns.heatmap(avg_macros, annot=True, fmt=".2f", cmap="YlOrRd", linewidths=0.5)
plt.title(f"Macronutrient Heatmap - {ts}")
plt.tight_layout()
plt.savefig("outputs/heatmap_macros.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: outputs/heatmap_macros.png")

# VIZ 3 — Scatter plot
plt.figure()
sns.scatterplot(data=top_protein, x="Protein(g)", y="Carbs(g)",
                hue="Diet_type", size="Fat(g)", sizes=(50, 400),
                alpha=0.7, palette="tab10")
plt.title(f"Top Protein Recipes Distribution - {ts}")
plt.tight_layout()
plt.savefig("outputs/scatter_top_protein.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: outputs/scatter_top_protein.png")

print("\n" + "="*50)
print("ANALYSIS COMPLETE")
print("="*50)
print(f"Completed at: {datetime.now()}")
