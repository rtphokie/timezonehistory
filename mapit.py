import unittest
from pprint import pprint
import matplotlib.pyplot as plt
import geopandas
import pandas as pd
import pytz
import pyproj
from dst_legislation_data import legislation

pd.set_option("display.max_rows", None, "display.max_columns", None)

states = geopandas.read_file('data/usa-states-census-2014.shp')

def visualize_dst_legislation():
    fig, ax = plt.subplots(figsize=(16, 9))
    #
    df = geopandas.read_file('data/cb_2018_us_state_20m.shp')
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

    def test_tz(self):
        import random
        tzs = geopandas.read_file('data/world/tz_world_mp.shp')
        tzs = tzs.to_crs("EPSG:3395")
        tzs = tzs[~tzs['TZID'].str.contains('uninhabited')]
        print(tzs['TZID'])
        tzs['coords'] = tzs['geometry'].apply(lambda x: x.representative_point().coords[:])
        tzs['coords'] = [coords[0] for coords in tzs['coords']]
        tzs = tzs.reset_index()
        tzs = tzs.rename(columns={"index": "rule"})
        # tzs['New_ID'] = df.index + 880

        fig, ax = plt.subplots(figsize=(16, 9))
        tzs.plot(ax=ax, cmap='Paired', column='rule')

        # label
        for idx, row in tzs.iterrows():
            # print(row['TZID'], row['geometry'].area)
            if row['geometry'].area > 50:
                plt.annotate(s=row['TZID'].replace('America/',''), xy=row['coords'],
                             horizontalalignment='center')
        # ax.set_xlim(-180, -40)
        # ax.set_ylim(15, 80)
        plt.tight_layout()
        # plt.savefig('tzmap.png', dpi=600)
        plt.show()


if __name__ == '__main__':
    #visualize_dst_legislation()
    unittest.main()
