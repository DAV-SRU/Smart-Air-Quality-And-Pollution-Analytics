"""Smart Air Quality & Pollution Analytics - Issue #10
Run:  python analysis.py   (needs city_day.csv in the same folder)
Output: six charts in ./charts
"""
import os
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(HERE, "charts"); os.makedirs(CH, exist_ok=True)
sns.set_theme(style="whitegrid")

df = pd.read_csv(os.path.join(HERE, "city_day.csv"), parse_dates=["Datetime"])

# AQI category from AQI value using CPCB bands
labels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
df["AQI_Category"] = pd.cut(df.AQI, [-0.1, 50, 100, 200, 300, 400, 500], labels=labels)

def save(fig, name):
    fig.tight_layout(); fig.savefig(os.path.join(CH, name), dpi=150); plt.close(fig)

# 1. AQI over time (monthly average per city)
monthly = (df.set_index("Datetime").groupby("City").AQI.resample("MS").mean().reset_index())
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=monthly, x="Datetime", y="AQI", hue="City", linewidth=1.2, ax=ax)
ax.set(title="AQI Over Time (Monthly Average, 2015-2024)", xlabel="Date", ylabel="Average AQI")
sns.move_legend(ax, "upper left", bbox_to_anchor=(1.01, 1))
save(fig, "1_aqi_over_time.png")

# 2. City-wise average AQI
city = df.groupby("City").AQI.mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=city.index, y=city.values, hue=city.index, palette="viridis", legend=False, ax=ax)
for i, v in enumerate(city.values): ax.text(i, v + 2, f"{v:.1f}", ha="center")
ax.set(title="City-wise Average AQI", xlabel="City", ylabel="Average AQI")
save(fig, "2_citywise_average_aqi.png")

# 3. Average pollutant levels
pols = ["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]
avg = df[pols].mean()
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(x=pols, y=avg.values, hue=pols, palette="mako", legend=False, ax=ax)
for i, v in enumerate(avg.values): ax.text(i, v + 3, f"{v:.1f}", ha="center")
ax.set_xticks(range(len(pols))); ax.set_xticklabels(["PM2.5", "PM10", "NO\u2082", "CO", "SO\u2082", "O\u2083"])
ax.set(title="Average Pollutant Levels", xlabel="Pollutant", ylabel="Average concentration")
save(fig, "3_average_pollutant_levels.png")

# 4. Correlation heatmap (pollutants vs AQI)
cols = ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene", "AQI"]
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(df[cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, vmin=-1, vmax=1,
            annot_kws={"size": 7}, ax=ax)
ax.set_title("Correlation Heatmap: Pollutants and AQI")
save(fig, "4_correlation_heatmap.png")

# 5. AQI category distribution (number of days)
cnt = df.AQI_Category.value_counts().reindex(labels)
colors = ["#2e9e44", "#9acd32", "#f2d424", "#f28c28", "#e04b3a", "#8b1a1a"]
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(cnt.index.astype(str), cnt.values, color=colors)
for i, v in enumerate(cnt.values): ax.text(i, v + 60, f"{v:,}", ha="center")
ax.set(title="AQI Category Distribution (Number of City-Days)", xlabel="AQI category", ylabel="Number of days")
save(fig, "5_aqi_category_distribution.png")

# 6. PM2.5 vs AQI
r = df["PM2.5"].corr(df.AQI)
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(df["PM2.5"], df.AQI, s=6, alpha=0.25, color="#3b6ea5")
m, b = np.polyfit(df["PM2.5"], df.AQI, 1)
xs = np.array([df["PM2.5"].min(), df["PM2.5"].max()])
ax.plot(xs, m * xs + b, color="red", label=f"Trend line (r = {r:.3f})")
ax.set(title="PM2.5 vs AQI", xlabel="PM2.5 concentration", ylabel="AQI")
ax.legend()
save(fig, "6_pm25_vs_aqi.png")

print("Saved 6 charts to", CH)
