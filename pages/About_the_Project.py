import streamlit as st
import os

st.title("About the Project")
st.markdown("---")

# --- Project Overview ---
st.markdown("""
## Project Overview

This project explores Citi Bike mobility patterns in the **Jersey City / Hoboken** system using trip data from **January to March 2025**.

Our goal is to build an interactive web app that helps users understand:

- **when** Citi Bike rides happen most often,
- **where** activity is concentrated,
- and **how** stations are connected as a mobility network.

By organizing the project into temporal, spatial, and network sections, we aim to present a clear and readable picture of everyday urban biking patterns.
""")

st.markdown("---")

# --- Data Source ---
st.markdown("""
## Data Source

The project uses Citi Bike trip data from the official Citi Bike system data files.

We worked with trip-level ride data and created cleaned summary datasets for analysis and visualization.

### Dataset Preparation

Our cleaned data focuses on the **Jersey City / Hoboken** Citi Bike system and includes summary files used in the app:

- **`hourly_summary.csv`** — hourly ride counts for temporal analysis
- **`monthly_summary.csv`** — monthly ride totals and rider-type summaries
- **`od_edges.csv`** — station-to-station trip flows for network analysis

The data was cleaned and prepared to support interactive charts, maps, and network visualizations in Streamlit.
""")

st.markdown("---")

# --- What We Did ---
st.markdown("""
## What We Did

We built a set of interactive visualizations across three main sections:

### 1. Temporal Patterns
- Examined how Citi Bike usage changes by **hour of day**, **day of week**, and **month**
- Compared **weekday vs. weekend** riding patterns
- Compared **member vs. casual** rider behavior
- Used line charts, bar charts, and a heatmap to show time-based trends

### 2. Spatial Patterns
- Identified where Citi Bike activity is concentrated in **Jersey City and Hoboken**
- Visualized the **main activity centers** using an interactive map
- Highlighted the **busiest stations**
- Compared station activity across selected areas

### 3. Network Analysis
- Built a station-to-station network using:
  - **stations as nodes**
  - **trip flows as edges**
  - **trip counts as edge weights**
- Highlighted the **strongest routes**, **major hubs**, and **pairwise station connections**
- Used bar charts, a filtered network map, and an adjacency matrix heatmap
""")

st.markdown("---")

# --- Techniques Used ---
st.markdown("""
## Techniques Used

This project uses the following tools and techniques:

- **Streamlit** for the interactive web app
- **Pandas** for data cleaning and aggregation
- **Plotly** for interactive charts and maps
- **NetworkX** for network construction and network metrics
- **Matplotlib / Seaborn** for supporting visualizations
- **CSV summary files** to organize cleaned outputs for different project sections

Our design approach focused on keeping the layout simple, using consistent filters, and grouping charts by story: **time, space, and network**.
""")

st.markdown("---")

# --- Process Book ---
st.markdown("""
## Process Book

Below is a snapshot from our process book, which documents how the project developed from early planning sketches into the final Streamlit app.

### First Stage: Planning the App Structure
At the beginning of the project, we focused on deciding how to organize the app into clear sections and what kinds of charts would best answer our main questions.

We grouped the project into:
- **Home / introduction**
- **Temporal patterns**
- **Spatial patterns**
- **Network analysis**

### Second Stage: Designing the Visual Story
As the project developed, we refined the layout so that each section answered one major question:

- **When do people ride most?**
- **Where are the main activity centers?**
- **How are stations connected?**

We also added interactive filters to improve readability and make the app easier to explore.
""")

# --- Safe path construction for image ---
CURRENT_DIR = os.path.dirname(__file__)
IMAGE_PATH_1 = os.path.join(CURRENT_DIR, "..", "images", "process_book_1.png")

if os.path.exists(IMAGE_PATH_1):
    st.image(IMAGE_PATH_1, use_container_width=True)
else:
    st.info("Add your process book sketch image to: images/process_book_1.png")

st.markdown("---")

# --- Final Note ---
st.markdown("""
## Final Note

Overall, this project uses Citi Bike as a way to better understand urban mobility in the Jersey City / Hoboken area.

By combining temporal analysis, spatial visualization, and network analysis, we aim to present an accessible and engaging picture of how bike-share reflects the structure and rhythm of city life.
""")

st.markdown("---")
st.caption("© 2026 · QMSS Final Project")
