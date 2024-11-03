import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Load the flight route data from Excel
file_path = 'flight_route.xlsx'
data = pd.read_excel(file_path, engine='openpyxl')

# Load the shapefile for countries
shapefile_path = 'ne_110m_admin_0_countries.shp'
world = gpd.read_file(shapefile_path)
india = world[world['ADMIN'] == "India"]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the map of India
india.plot(ax=ax, color='lightgrey', edgecolor='black')

# Set up Basemap for plotting air routes
m = Basemap(projection='merc', llcrnrlat=5, urcrnrlat=37, llcrnrlon=65, urcrnrlon=100, resolution='i', ax=ax)

# Draw map boundaries and fill continents
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='lightgreen', lake_color='aqua')
m.drawcoastlines()
m.drawcountries()

# Plot each route and annotate with names
for idx, row in data.iterrows():
    source_lat, source_lon = row['Source_lat'], row['Source_lon']
    dest_lat, dest_lon = row['Dest_lat'], row['Dest_lon']
    source_name = row['Source']  # Source name column
    dest_name = row['Destination']      # Destination name column
    
    # Draw route line if coordinates are valid
    if pd.notnull(source_lat) and pd.notnull(source_lon) and pd.notnull(dest_lat) and pd.notnull(dest_lon):
        # Draw the great circle route
        m.drawgreatcircle(source_lon, source_lat, dest_lon, dest_lat, linewidth=1, color='blue')

        # Transform the lat/lon to the Basemap projection
        x_source, y_source = m(source_lon, source_lat)
        x_dest, y_dest = m(dest_lon, dest_lat)

        # Annotate with a circle ('o') and names
        plt.plot(x_source, y_source, 'o', markersize=5, color='black')  # Circle for source
        plt.text(x_source + 0.5, y_source, source_name, fontsize=8, ha='left', color='black', fontweight='bold')

        plt.plot(x_dest, y_dest, 'o', markersize=5, color='black')    # Circle for destination
        plt.text(x_dest + 0.5, y_dest, dest_name, fontsize=8, ha='left', color='black', fontweight='bold')

# Add map details and display
plt.title('Air Routes within India')
plt.show()
