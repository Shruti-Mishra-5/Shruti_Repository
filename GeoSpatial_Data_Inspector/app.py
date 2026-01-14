import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.validation import make_valid
import folium
from streamlit_folium import st_folium
import tempfile
import zipfile
import os

st.set_page_config(page_title="GeoSpatial Data Inspector", layout="wide")

st.title("🗺️ GeoSpatial_Data_Inspector")
st.caption("Inspect, validate, and clean geospatial datasets")

# ---------------- FILE UPLOAD ---------------- #
uploaded_file = st.file_uploader(
    "Upload a geospatial file",
    type=["geojson", "json", "zip", "gpkg", "kml", "csv"]
)

# ---------------- LOAD DATA FUNCTION ---------------- #
def load_data(file, lat_col=None, lon_col=None):
    name = file.name.lower()

    # GeoJSON
    if name.endswith((".geojson", ".json")):
        return gpd.read_file(file)

    # GeoPackage
    if name.endswith(".gpkg"):
        return gpd.read_file(file)

    # KML
    if name.endswith(".kml"):
        return gpd.read_file(file, driver="KML")

    # Shapefile ZIP
    if name.endswith(".zip"):
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "data.zip")
            with open(zip_path, "wb") as f:
                f.write(file.read())

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(tmpdir)

            shp_files = [f for f in os.listdir(tmpdir) if f.endswith(".shp")]
            if not shp_files:
                st.error("No .shp file found in ZIP.")
                return None

            return gpd.read_file(os.path.join(tmpdir, shp_files[0]))

    # CSV with coordinates (OPTIONAL)
    if name.endswith(".csv") and lat_col and lon_col:
        df = pd.read_csv(file)
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
            crs="EPSG:4326"
        )
        return gdf

    return None

# ---------------- MAIN LOGIC ---------------- #
if uploaded_file:

    lat_col = lon_col = None

    # CSV-specific UI
    if uploaded_file.name.lower().endswith(".csv"):
        st.info("CSV detected — select coordinate columns")
        df_preview = pd.read_csv(uploaded_file)
        cols = df_preview.columns.tolist()

        lat_col = st.selectbox("Latitude column", cols)
        lon_col = st.selectbox("Longitude column", cols)

    gdf = load_data(uploaded_file, lat_col, lon_col)

    if gdf is not None:
        st.success("Dataset loaded successfully!")

        # ---------------- BASIC INFO ---------------- #
        st.subheader("📊 Dataset Overview")
        col1, col2, col3 = st.columns(3)

        col1.metric("Features", len(gdf))
        col2.metric("Attributes", len(gdf.columns) - 1)
        col3.metric("CRS", str(gdf.crs))

        # ---------------- CRS FIX ---------------- #
        st.subheader("🌐 CRS Inspection")

        if gdf.crs is None:
            st.warning("CRS is missing!")
        else:
            st.info(f"Current CRS: {gdf.crs}")

        new_epsg = st.text_input("Reproject to EPSG (optional)", value="")

        if st.button("Fix / Reproject CRS"):
            try:
                epsg_code = int(new_epsg)
                gdf = gdf.set_crs(epsg=epsg_code, allow_override=True)
                gdf = gdf.to_crs(epsg=epsg_code)
                st.success(f"Reprojected to EPSG:{epsg_code}")
            except:
                st.error("Invalid EPSG code")

        # ---------------- GEOMETRY CHECK ---------------- #
        st.subheader("🧩 Geometry Health Check")

        invalid_count = (~gdf.is_valid).sum()
        empty_count = gdf.geometry.is_empty.sum()

        col1, col2 = st.columns(2)
        col1.metric("Invalid Geometries", invalid_count)
        col2.metric("Empty Geometries", empty_count)

        if st.button("Fix Invalid Geometries"):
            gdf["geometry"] = gdf["geometry"].apply(
                lambda geom: make_valid(geom) if geom and not geom.is_valid else geom
            )
            st.success("Invalid geometries repaired")

        # ---------------- ATTRIBUTE INSPECTION ---------------- #
        st.subheader("📋 Attribute Inspection")

        attr_df = pd.DataFrame({
            "Column": gdf.columns,
            "Data Type": gdf.dtypes.astype(str),
            "Missing %": (gdf.isnull().mean() * 100).round(2)
        })

        st.dataframe(attr_df, use_container_width=True)

        # ---------------- MAP VISUALIZATION ---------------- #
        st.subheader("🗺️ Spatial Visualization")

        gdf_map = gdf.to_crs(epsg=4326)

        m = folium.Map(
            location=[
                gdf_map.geometry.centroid.y.mean(),
                gdf_map.geometry.centroid.x.mean()
            ],
            zoom_start=6,
            tiles="CartoDB positron"
        )

        folium.GeoJson(
            gdf_map,
            tooltip=folium.GeoJsonTooltip(
                fields=[col for col in gdf_map.columns if col != "geometry"]
            )
        ).add_to(m)

        st_folium(m, width=1100, height=500)

        # ---------------- DOWNLOAD ---------------- #
        st.subheader("⬇️ Export Cleaned Data")

        cleaned_geojson = gdf_map.to_json()

        st.download_button(
            label="Download as GeoJSON",
            data=cleaned_geojson,
            file_name="cleaned_data.geojson",
            mime="application/json"
        )
