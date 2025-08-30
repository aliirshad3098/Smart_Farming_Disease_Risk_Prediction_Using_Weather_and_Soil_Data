import os
import pandas as pd

# Paths define karo 
base_dir = "OSBS_datasets"   # jis folder me sab products hain
products = {
    "Soil_CO2_concentration": "DP1.00095.001",
    "Soil_temperature": "DP1.00041.001",
    "Soil_water_content_and_salinity": "DP1.00094.001",
    "Wind_speed_and_direction": "DP1.00001.001",
    "Relative_humidity": "DP1.00098.001",
    "Precipitation": "DP1.00006.001"
}

# Har product ka 6 month combine karna 
for product_name in products.keys():
    folder = os.path.join(base_dir, product_name)
    all_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".csv")]

    # sirf 2021-01 to 2021-06 wale files rakhna
    all_files = [f for f in all_files if any(m in f for m in ["2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06"])]

    df_list = []
    for file in sorted(all_files):
        try:
            df = pd.read_csv(file)

            # yahan endDateTime column hata diya
            if "endDateTime" in df.columns:
                df.drop(columns=["endDateTime"], inplace=True)
            # yahan pr extra column remove kia jo ek datafile me present tha
            if os.path.basename(file) == "Precipitation_OSBS_2021-01_1min.csv":
                df.drop(columns=["secPrecipHeater0QM","secPrecipHeater1QM","secPrecipHeater2QM","secPrecipHeater3QM"], inplace=True)
            
            df_list.append(df)
        except Exception as e:
            print(f"rror reading {file}: {e}")

    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        combined_path = os.path.join(folder, "combined.csv")
        combined_df.to_csv(combined_path, index=False)
        print(f"Combined saved for {product_name}: {combined_path}")
    else:
        print(f"No files found for {product_name}")

# Final merge across all products 
merged_final = None

for product_name in products.keys():
    combined_path = os.path.join(base_dir, product_name, "combined.csv")
    if os.path.exists(combined_path):
        df = pd.read_csv(combined_path)

        # yahan hm ensure karrha hai ki har product me 'datetime' column ho
        if "datetime" not in df.columns:
            if "startDateTime" in df.columns:
                df.rename(columns={"startDateTime": "datetime"}, inplace=True)

        # ab merge karte hain
        if merged_final is None:
            merged_final = df
        else:
            merged_final = pd.merge(merged_final, df, on="datetime", how="outer")

# save final merged file
final_dir = os.path.join(base_dir, "merged_final")
os.makedirs(final_dir, exist_ok=True)

final_path = os.path.join(final_dir, "combined.csv")
merged_final.to_csv(final_path, index=False)

print(f"\nFinal merged dataset saved at: {final_path}")
