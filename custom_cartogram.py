import pandas as pd
import numpy as np
import altair as alt
import vega_datasets
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon

def plot_choropleth(gdf, column, cmap='viridis', legend=True):
    """
    Plot a basic choropleth map.

    Parameters:
        gdf: GeoDataFrame
            The GeoDataFrame containing the geometries and data to plot.
        column: str
            The column name to use for coloring the choropleth.
        cmap: str, optional
            The colormap to use. Default is 'viridis'.
        legend: bool, optional
            Whether to add a legend. Default is True.
    """
    fig, ax = plt.subplots(figsize=(12, 12))
    # Create a colormap
    vmin, vmax = gdf[column].min(), gdf[column].max()
    # Create a ScalarMappable for color normalization
    sm = plt.cm.ScalarMappable(cmap=cmap, 
                               norm=plt.Normalize(vmin=vmin, 
                                                 vmax=vmax))
    # Ensure the mappable is initialized
    sm._A = []
    # Iterate through each geometry and plot
    for idx, row in gdf.iterrows():
        plot_polygon(ax, row['geometry'], row[column], sm, vmin, vmax)
        
    if legend:
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label(column, rotation=270, labelpad=15)
        
    plt.axis('equal')
    plt.show()

def plot_polygon(ax, polygon, value, sm, vmin, vmax):
    if isinstance(polygon, Polygon):
        # Plotting for a Polygon
        x, y = polygon.exterior.xy
        color = sm.cmap((value - vmin) / (vmax - vmin)) # Normalize the value
        ax.fill(x, y, color=color)
        
    elif isinstance(polygon, MultiPolygon):
        #print(f"MultiPolygon with {len(polygon.geoms)} polygons.")  # Debugging line
        # Plotting for a MultiPolygon
        for poly in polygon.geoms:
            x, y = poly.exterior.xy
            color = sm.cmap((value - vmin) / (vmax - vmin))  # Normalize the value
            ax.fill(x, y, color=color)
            
    else:
        raise ValueError(f"Unknown geometry type {type(polygon)} encountered.")


# Example usage
#gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#plot_choropleth(gdf, 'gdpPercap', cmap='viridis')