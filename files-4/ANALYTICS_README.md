# Data Analytics (Issue #10) – Smart Air Quality & Pollution Analytics

**Dataset:** `city_day.csv` – 18,265 daily records, 5 cities (Delhi, Mumbai, Chennai, Kolkata, Bangalore), 2015-01-01 to 2024-12-31; 12 pollutants, AQI and AQI_Bucket. No missing values or duplicates.
**Run:** `pip install pandas matplotlib seaborn` then `python analysis.py` (charts are saved in `charts/`).

## Charts
| # | Chart | Shows |
|---|---|---|
| 1 | `1_aqi_over_time.png` | Monthly average AQI per city, 2015–2024 |
| 2 | `2_citywise_average_aqi.png` | Average AQI compared across cities |
| 3 | `3_average_pollutant_levels.png` | Average PM2.5, PM10, NO₂, CO, SO₂ and O₃ |
| 4 | `4_correlation_heatmap.png` | Correlation between pollutants and AQI |
| 5 | `5_aqi_category_distribution.png` | Number of days in each AQI category |
| 6 | `6_pm25_vs_aqi.png` | PM2.5 vs AQI scatter with trend line |

## Notes
- AQI categories (chart 5) are computed from the AQI value using CPCB bands (Good 0–50, Satisfactory 51–100, Moderate 101–200, Poor 201–300, Very Poor 301–400, Severe 401–500). The dataset's own `AQI_Bucket` column disagrees with these bands in about 84% of rows, so it was not used.
- Mean AQI is almost identical across cities (Mumbai 253.3 highest, Bangalore 249.8 lowest), AQI shows no clear trend or seasonality, and no pollutant correlates with AQI (|r| < 0.02, PM2.5 r = 0.001). Pollutant values are spread almost uniformly, which is unlike real monitoring data and suggests the dataset is synthetic. These results describe this dataset only.
