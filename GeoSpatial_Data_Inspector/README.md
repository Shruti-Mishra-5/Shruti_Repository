# GeoSpatial_Data_Inspector

A lightweight Streamlit-based GIS utility for inspecting, validating, and cleaning vector geospatial datasets prior to analysis or visualization.

This tool is designed to handle common real-world geospatial data issues such as missing CRS information, invalid geometries, inconsistent schemas, and poor data quality.

---

## Features

### 1. Multi-format Geospatial Data Ingestion
Supports common vector geospatial formats:
- **GeoJSON** (`.geojson`, `.json`)
- **ESRI Shapefile** (zipped `.zip`)
- **GeoPackage** (`.gpkg`)
- **KML** (`.kml`)
- **CSV with coordinates** (`.csv`, point data only)

> CSV support requires latitude and longitude columns selected by the user and assumes EPSG:4326.

---

### 2. Dataset Overview & Metadata Inspection
- Displays total number of spatial features
- Displays attribute count (excluding geometry)
- Detects and reports Coordinate Reference System (CRS)
- Flags datasets with missing or undefined CRS

---

### 3. CRS Validation & Reprojection
- Identifies missing CRS definitions
- Allows manual CRS assignment using EPSG codes
- Supports reprojection to user-specified CRS
- Ensures spatial alignment for downstream GIS operations

---

### 4. Geometry Health Checks & Repair
- Detects invalid geometries (self-intersections, topology errors)
- Detects empty geometries
- Repairs invalid geometries using Shapely’s validation tools
- Prepares datasets for reliable spatial analysis

---

### 5. Attribute Table Inspection (Spatial EDA)
- Lists all attribute fields
- Displays data types per column
- Computes percentage of missing values per attribute
- Enables rapid identification of low-quality or sparse fields

---

### 6. Interactive Spatial Visualization
- Automatically reprojects data to WGS84 (EPSG:4326) for web mapping
- Generates interactive maps using Folium
- Dynamically centers map using feature centroids
- Supports attribute-based tooltips for spatial inspection
- Uses clean, minimal basemap styling (CartoDB Positron)

---

### 7. Clean Data Export
- Exports validated and cleaned spatial data
- Outputs standardized **GeoJSON** format
- Ensures consistent CRS and valid geometries

---

## Tech Stack

- **Python**
- **Streamlit**
- **GeoPandas**
- **Shapely**
- **PyProj**
- **Pandas**
- **Folium**
- **streamlit-folium**

---

## Project Structure
GeoSpatial_Data_Inspector/
│
├── app.py
├── requirements.txt
└── README.md


---

## Installation & Usage
```bash
pip install -r requirements.txt
streamlit run app.py


Author
Shruti Mishra