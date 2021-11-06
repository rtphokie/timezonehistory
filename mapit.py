import unittest
from pprint import pprint
import matplotlib.pyplot as plt
import geopandas
import pandas as pd
import pytz
import pyproj
from data import legislation, possible_rules
from parse_zdump import timezone_rules

pd.set_option("display.max_rows", None, "display.max_columns", None)

states = geopandas.read_file('data/usa-states-census-2014.shp')

def plottzs(label=False, world=False):
    #https://proj.org/
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_aspect('equal')

    gdf = geopandas.read_file('data/world/tz_world_mp.shp')
    gdf = gdf[~gdf['TZID'].str.contains('uninhabited')] #don't plot Antartica
    gdf['coords'] = gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
    gdf['coords'] = [coords[0] for coords in gdf['coords']]
    gdf = gdf.reset_index()
    gdf = gdf.rename(columns={"index": "rule"})
    # minx, miny, maxx, maxy = gdf.total_bounds
    # print(minx, miny, maxx, maxy)

    if world:
        mill = pyproj.Proj(proj='robin', ellps='WGS84', datum='WGS84')
        gdf = gdf.to_crs(crs=mill.srs)
    else: # CONUS
        mill = pyproj.Proj(proj='mill', ellps='WGS84', datum='WGS84')
        ax.set_xlim(-180, -50)
        ax.set_ylim(15,75)


    cmap = plt.cm.get_cmap("OrRd").copy()
    cmap.set_bad(color='black')

    gdf.plot(ax=ax, cmap=cmap, column='rule',edgecolor='black')

    # label
    if label:
        for idx, row in gdf.iterrows():
            # print(row['TZID'], row['geometry'].area)
            if row['geometry'].area > 50:
                plt.annotate(s=row['TZID'].replace('America/', ''), xy=row['coords'],
                             horizontalalignment='center')
    ax.axis('off')
    plt.tight_layout()
    # plt.savefig('tzmap.png', dpi=600)
    plt.show()

def visualize_dst_legislation():
    fig, ax = plt.subplots(figsize=(16, 9))
    #
    gdf = geopandas.read_file('data/cb_2018_us_state_20m.shp')
    aeqd = pyproj.Proj(proj='aeqd', ellps='WGS84', datum='WGS84', lat_0=39.0, lon_0=-98.5).srs
    df = df.to_crs(crs=aeqd)  #switch to mercator projection around US centroid

    # map legislation status onto a new column
    df['LEG'] = df['NAME'].str.lower().map(legislation)

    df.plot(cmap='viridis', column='LEG', ax=ax, edgecolor='black')
    plt.tight_layout()
    plt.savefig('dst_legislation.png', dpi=600)


class MyTestCase(unittest.TestCase):

    def test_us_counties(self):
        states = geopandas.read_file('data/cb_2018_us_county_20m.shp')
        states = states.to_crs("EPSG:3395")
        states.plot()
        plt.show()

    def test_plot_CONUS_tz_rules(self):
        tzs = pytz.country_timezones['US']
        tzs += pytz.country_timezones['CA']
        result, result2 = timezone_rules(tzs, simplifyranges=False)
        plottzs()

    def test_plot_CONUS_tz(self):
        plottzs()

    def test_plot_world_tz(self):
        plottzs(world=True)



if __name__ == '__main__':
    #visualize_dst_legislation()
    unittest.main()
