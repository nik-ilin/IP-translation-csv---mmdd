
import pandas as pd
import ipaddress
from pathlib import Path

blocks_src   = Path("GeoLite2-Country-Blocks-IPv4.csv") 
locations_ru = Path("GeoLite2-Country-Locations-ru.csv")
blocks_out   = Path("GeoLite2-Country-FINAL.csv")

target_networks = {
    "176.99.96.0/19",
    "91.237.182.0/23",
    "188.114.208.0/20",
}

df  = pd.read_csv(blocks_src, dtype=str)        
loc = pd.read_csv(locations_ru, usecols=["geoname_id", "country_iso_code"])

if target_networks:
    try:
        ru_id = int(loc.loc[loc.country_iso_code == "RU", "geoname_id"].iloc[0])
    except IndexError:
        raise RuntimeError("В Locations‑ru.csv нет строки с кодом RU")
    mask = df["network"].isin(target_networks)
    df.loc[mask, ["geoname_id", "registered_country_geoname_id"]] = str(ru_id)
    print(f"✔️  Lines overwritten: {mask.sum()}")

def cidr_to_range(cidr: str):

    if not isinstance(cidr, str) or cidr.strip() == "":
        return pd.Series([None, None])

    clean = cidr.strip().strip('"').strip("'").split(";")[0]
    try:
        net = ipaddress.ip_network(clean, strict=False)
        return pd.Series([int(net.network_address), int(net.broadcast_address)])
    except ValueError:
        return pd.Series([None, None])

df[["start_ip_int", "end_ip_int"]] = df["network"].apply(cidr_to_range)

bad_rows = df["start_ip_int"].isna().sum()
if bad_rows:
    print(f"Missed {bad_rows} by CIDR")
df = df.dropna(subset=["start_ip_int", "end_ip_int"])

num_cols = [
    "geoname_id", "registered_country_geoname_id",
    "represented_country_geoname_id",
    "is_anonymous_proxy", "is_satellite_provider", "is_anycast",
]
for col in num_cols:
    df[col] = (
        df[col]                   
        .fillna(0)
        .replace("", 0)
        .astype(float)
        .astype(int)
    )

out_cols = [
    "start_ip_int", "end_ip_int",
    *num_cols,
]
df[out_cols].to_csv(blocks_out, index=False)
print(f"Done! Rows in total: {len(df):,}")