import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import shutil

Path("/mnt/data").mkdir(exist_ok=True)

output_dir = Path("/mnt/data/section3_outputs")
output_dir.mkdir(exist_ok=True)

# Original file paths in /content/
source_data_files = [
    "/content/JC-202501-citibike-tripdata.csv",
    "/content/JC-202502-citibike-tripdata.csv",
    "/content/JC-202503-citibike-tripdata.csv",
    "/content/JC-202504-citibike-tripdata.csv",
    "/content/JC-202505-citibike-tripdata.csv"
]

# New target paths in /mnt/data/
data_files = []
for src_file in source_data_files:
    dest_file = Path("/mnt/data/") / Path(src_file).name
    shutil.copy(src_file, dest_file)
    data_files.append(str(dest_file))

df = pd.concat(
    [pd.read_csv(file) for file in data_files],
    ignore_index=True
)

df["started_at"] = pd.to_datetime(df["started_at"], errors="coerce")
df["ended_at"] = pd.to_datetime(df["ended_at"], errors="coerce")

df["ride_duration_min"] = (
    df["ended_at"] - df["started_at"]
).dt.total_seconds() / 60

df = df[
    (df["ride_duration_min"] > 0) &
    (df["ride_duration_min"] <= 24 * 60)
].copy()

df = df.dropna(
    subset=[
        "start_station_name",
        "start_station_id",
        "start_lat",
        "start_lng"
    ]
)

start_station_activity = (
    df.groupby(
        ["start_station_id", "start_station_name", "start_lat", "start_lng"],
        dropna=False
    )
    .size()
    .reset_index(name="start_trips")
)

end_station_activity = (
    df.dropna(
        subset=[
            "end_station_name",
            "end_station_id",
            "end_lat",
            "end_lng"
        ]
    )
    .groupby(
        ["end_station_id", "end_station_name", "end_lat", "end_lng"],
        dropna=False
    )
    .size()
    .reset_index(name="end_trips")
)

station_activity = start_station_activity.merge(
    end_station_activity,
    left_on="start_station_id",
    right_on="end_station_id",
    how="outer"
)

station_activity["station_id"] = station_activity["start_station_id"].fillna(
    station_activity["end_station_id"]
)

station_activity["station_name"] = station_activity["start_station_name"].fillna(
    station_activity["end_station_name"]
)

station_activity["lat"] = station_activity["start_lat"].fillna(
    station_activity["end_lat"]
)

station_activity["lng"] = station_activity["start_lng"].fillna(
    station_activity["end_lng"]
)

station_activity["start_trips"] = station_activity["start_trips"].fillna(0)
station_activity["end_trips"] = station_activity["end_trips"].fillna(0)
station_activity["total_trips"] = (
    station_activity["start_trips"] + station_activity["end_trips"]
)

station_activity = station_activity[
    [
        "station_id",
        "station_name",
        "lat",
        "lng",
        "start_trips",
        "end_trips",
        "total_trips"
    ]
].copy()

def assign_city_area(row):
    name = str(row["station_name"]).lower()
    lat = row["lat"]
    lng = row["lng"]

    hoboken_keywords = [
        "hoboken",
        "washington st",
        "clinton st",
        "hudson st",
        "river st",
        "shipyard",
        "church sq",
        "monroe st",
        "madison st",
        "columbus park",
        "mama johnson",
        "sinatra",
        "11 st",
        "8 st",
        "6 st & grand",
        "14 st ferry",
        "city hall - washington",
        "bloomfield",
        "grand st & 2 st",
        "adams st",
        "jackson st",
        "marshall st",
        "willow ave"
    ]

    if any(keyword in name for keyword in hoboken_keywords):
        return "Hoboken"

    if lat >= 40.735 and lng >= -74.045:
        return "Hoboken"

    return "Jersey City"


station_activity["area"] = station_activity.apply(assign_city_area, axis=1)

station_activity.to_csv(
    output_dir / "station_activity_clean_area.csv",
    index=False
)

display(
    station_activity
    .groupby("area", as_index=False)
    .agg(
        total_trips=("total_trips", "sum"),
        start_trips=("start_trips", "sum"),
        end_trips=("end_trips", "sum"),
        station_count=("station_id", "nunique")
    )
)

fig8 = px.scatter_mapbox(
    station_activity,
    lat="lat",
    lon="lng",
    size="total_trips",
    color="area",
    hover_name="station_name",
    hover_data={
        "area": True,
        "start_trips": ":,.0f",
        "end_trips": ":,.0f",
        "total_trips": ":,.0f",
        "lat": False,
        "lng": False
    },
    size_max=35,
    zoom=11.3,
    height=700,
    title="Chart 8. Interactive Station Activity Map: Jersey City / Hoboken Citi Bike Activity"
)

fig8.update_layout(
    mapbox_style="carto-positron",
    margin=dict(l=0, r=0, t=60, b=0),
    legend_title_text="Area"
)

fig8.write_html(output_dir / "chart8_station_activity_map_clean.html")
fig8.show()

top10_stations = (
    station_activity
    .sort_values("total_trips", ascending=False)
    .head(10)
    .sort_values("total_trips", ascending=True)
)

fig9 = px.bar(
    top10_stations,
    x="total_trips",
    y="station_name",
    color="area",
    orientation="h",
    text="total_trips",
    hover_data={
        "area": True,
        "start_trips": ":,.0f",
        "end_trips": ":,.0f",
        "total_trips": ":,.0f"
    },
    title="Chart 9. Top 10 Busiest Citi Bike Stations"
)

fig9.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig9.update_layout(
    xaxis_title="Total Trips",
    yaxis_title="Station",
    height=580,
    margin=dict(l=230, r=80, t=70, b=50),
    legend_title_text="Area"
)

fig9.write_html(output_dir / "chart9_top10_busiest_stations_clean.html")
fig9.show()

area_activity = (
    station_activity
    .groupby("area", as_index=False)
    .agg(
        total_trips=("total_trips", "sum"),
        start_trips=("start_trips", "sum"),
        end_trips=("end_trips", "sum"),
        station_count=("station_id", "nunique")
    )
    .sort_values("total_trips", ascending=True)
)

fig10 = px.bar(
    area_activity,
    x="total_trips",
    y="area",
    orientation="h",
    text="total_trips",
    hover_data={
        "start_trips": ":,.0f",
        "end_trips": ":,.0f",
        "total_trips": ":,.0f",
        "station_count": ":,.0f"
    },
    title="Chart 10. Area-Level Citi Bike Activity: Jersey City vs Hoboken"
)

fig10.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig10.update_layout(
    xaxis_title="Total Trips",
    yaxis_title="Area",
    height=420,
    margin=dict(l=140, r=90, t=70, b=50)
)

fig10.write_html(output_dir / "chart10_area_level_trip_volume_clean.html")
fig10.show()

display(area_activity.sort_values("total_trips", ascending=False))

fig11 = px.density_mapbox(
    station_activity,
    lat="lat",
    lon="lng",
    z="total_trips",
    radius=18,
    center={
        "lat": station_activity["lat"].mean(),
        "lon": station_activity["lng"].mean()
    },
    zoom=11.3,
    height=700,
    title="Chart 11. Weighted Citi Bike Station Activity Hotspot Map"
)

fig11.update_layout(
    mapbox_style="carto-positron",
    margin=dict(l=0, r=0, t=60, b=0)
)

fig11.write_html(output_dir / "chart11_weighted_station_hotspot_map_clean.html")
fig11.show()
