import os
import requests
from datetime import datetime

API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJhdWQiOiJodHRwczovL2RhdGEubmVvbnNjaWVuY2Uub3JnL2FwaS92MC8iLCJzdWIiOiJhbGkuaXJzaGFkMzA5OEBnbWFpbC5jb20iLCJzY29wZSI6InJhdGU6cHVibGljIiwiaXNzIjoiaHR0cHM6Ly9kYXRhLm5lb25zY2llbmNlLm9yZy8iLCJleHAiOjE5MTQxNjg0MjcsImlhdCI6MTc1NjQ4ODQyNywiZW1haWwiOiJhbGkuaXJzaGFkMzA5OEBnbWFpbC5jb20ifQ.uUzvBRKbZjW24kv1PU760a61HKuw5GueeAh5IlAmLUDRD5tZvfQ4optx5KybXmPLasXkrvJCVbugaUFZvjuAEA"
BASE_URL = "https://data.neonscience.org/api/v0/data"

# Tumhara dataset mapping
DATASETS = {
    "Soil_CO2_concentration": "DP1.00095.001",
    "Soil_temperature": "DP1.00041.001",
    "Soil_water_content_and_salinity": "DP1.00094.001",
    "Wind_speed_and_direction": "DP1.00001.001",
    "Relative_humidity": "DP1.00098.001",
    "Precipitation": "DP1.00006.001",
}

# Download function
def fetch_dataset(product_code, site, date, save_dir, dataset_name):
    url = f"{BASE_URL}/{product_code}/{site}/{date}"
    headers = {"X-API-Token": API_TOKEN}

    response = requests.get(url, headers=headers)
    print(f"\n📥 Fetching {dataset_name} ({product_code}) for {site} {date}")
    print("Status Code:", response.status_code)

    try:
        data = response.json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return

    if "data" not in data or "files" not in data["data"]:
        print(f"No data found for {site} {date}")
        return

    files = data["data"]["files"]
    if not files:
        print(f"No files in response for {site} {date}")
        return
    else:
        print(f"{len(files)} files found")

    os.makedirs(save_dir, exist_ok=True)

    # ---- Filter for _1_minute files ----
    one_min_files = [f for f in files if ("_1_minute" in f["name"] or "1min" in f["name"])]

    if one_min_files:
        # Sirf pehli 1_minute file
        f = one_min_files[0]
        fname = os.path.join(save_dir, f"{dataset_name}_{site}_{date}_1min.csv")
        if os.path.exists(fname):
            print("⏩ Skipped (already downloaded):", fname)
            return
        try:
            csv_data = requests.get(f["url"], headers=headers)
            with open(fname, "wb") as out:
                out.write(csv_data.content)
            print("✔️ Downloaded (1_min):", fname)
        except Exception as e:
            print("Error downloading file:", f["name"], "|", e)
        return   # yahan return lagana zaroori hai

    # Agar koi 1_minute wali file hi nahi mili to doosri files download ho
    for f in files:
        fname = os.path.join(save_dir, f["name"])
        if os.path.exists(fname):
            print(" Skipped (already downloaded):", fname)
            continue
        try:
            csv_data = requests.get(f["url"], headers=headers)
            with open(fname, "wb") as out:
                out.write(csv_data.content)
            print("✔️ Downloaded:", fname)
        except Exception as e:
            print("Error downloading file:", f["name"], "|", e)

# Month range generator
def month_range(start, end):
    start_date = datetime.strptime(start, "%Y-%m")
    end_date = datetime.strptime(end, "%Y-%m")

    while start_date <= end_date:
        yield start_date.strftime("%Y-%m")
        # next month
        if start_date.month == 12:
            start_date = start_date.replace(year=start_date.year + 1, month=1)
        else:
            start_date = start_date.replace(month=start_date.month + 1)

# Loop through all datasets and multiple months
site = "OSBS"                 # Site code (e.g., HARV, SRER etc.)
start_date = "2021-01"        # Start month
end_date = "2021-06"          # End month
save_dir = "OSBS_datasets"

for name, code in DATASETS.items():
    dataset_dir = os.path.join(save_dir, name)
    for date in month_range(start_date, end_date):
        fetch_dataset(code, site, date, dataset_dir, name)
