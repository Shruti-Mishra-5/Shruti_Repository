# Drought Severity Mapping in Vidarbha, Maharashtra  
### Geospatial Analytics – CIA 2

## Project Overview
This project analyzes drought severity across the Vidarbha region of Maharashtra using geospatial methods. The study integrates vegetation and rainfall anomaly indicators to identify districts experiencing potential drought stress. The objective is to demonstrate how remote sensing and GIS can be used for drought assessment and decision support.

---

## Study Description
Drought is a major environmental hazard caused by prolonged low precipitation, leading to vegetation loss, water shortages, and economic stress in agricultural regions.  
This study combines two core indicators:

1. **NDVI (Normalized Difference Vegetation Index)** – to measure vegetation health  
2. **Rainfall Anomaly** – to assess deviations from normal rainfall patterns  

By overlaying these two layers, drought-prone areas were identified based on vegetation loss and rainfall deficit.

---

## Methodology

### Data Used
| Dataset | Purpose |
|---------|---------|
| NDVI Raster | Vegetation condition mapping |
| Rainfall Rasters (2015 and 2025) | Rainfall anomaly computation |
| Maharashtra District Boundary | Regional boundary and Vidarbha extraction |

### Process Workflow

1. **NDVI Data**
   - NDVI raster for India downloaded from Bhuvan Portal
   - Maharashtra district boundaries obtained from OpenCityMap
   - Vidarbha districts selected and exported as a separate layer

2. **Rainfall Anomaly**
   - Two rainfall raster layers (2015 and 2025) imported
   - Raster Calculator used to compute anomaly  
     (Anomaly = Current Year – Baseline Year)
   - Result clipped to Vidarbha boundary

3. **Final Drought Map**
   - NDVI visualized in green gradient  
   - Rainfall anomaly visualized in blue gradient  
   - Combined interpretation:
     - Dark blue + light vegetation = drought stress
     - Green + mild blue = no drought

---

## Key Findings

- Districts such as **Akola, Washim, Yavatmal, and Amravati** show low vegetation and rainfall, indicating drought conditions.
- **Gadchiroli, Chandrapur, and Gondia** show healthier vegetation and better rainfall.
- Drought severity varies spatially across Vidarbha rather than being uniform.
- The study highlights how geospatial analysis can support agricultural drought monitoring without relying solely on field surveys.

---

## Significance
This project demonstrates operational use of:

- Remote sensing data for drought assessment
- GIS‐based spatial extraction and raster analysis
- Layer-based visualization to support decision making

The method can be extended for:

- Seasonal drought forecasting  
- Risk mapping for vulnerable communities  
- Planning targeted relief interventions

---

## Software Used
- QGIS 3.x
- Raster Calculator
- Vector Selection and Clipping Tools

---

## Data Sources

1. **National Remote Sensing Centre (Bhuvan Portal)**  
   OCM2-GP India NDVI Dataset  
   Retrieved October 30, 2025

2. **OpenCity Data Portal**  
   Maharashtra District Boundary KML  
   https://data.opencity.in

3. **CHIRPS Rainfall Dataset**  
   Funk et al. (2015), Scientific Data, 2:150066  
   https://data.chc.ucsb.edu/products/CHIRPS-2.0/

4. **India Meteorological Department (IMD)**  
   State and District-wise Rainfall Records  
   https://mausam.imd.gov.in

5. **GADM Database**  
   Administrative Boundary Dataset  
   https://gadm.org

---
## Final Drought Severity Map

![Drought Map](images/Vidarbha_Map_Drought_Image.png)
