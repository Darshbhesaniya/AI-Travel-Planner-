import pandas as pd

df = pd.read_csv("airports.csv")

india = df[
    (df["iso_country"] == "IN") & 
    (df["scheduled_service"] == "yes") &
    (df["iata_code"].notna()) 
][["name","municipality","iata_code","iso_region","latitude_deg","longitude_deg"]]

india = india.rename(columns={
    "latitude_deg": "latitude",
    "longitude_deg": "longitude"
})
india["municipality"] = india["municipality"].fillna(india["name"])

india.to_json("data/airports_india.json", orient="records", indent=2)

print(len(india), "airports saved")