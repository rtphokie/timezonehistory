import unittest
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib as mpl
import geopandas
import pandas as pd
import pytz
import pyproj
import numpy as np
from data import legislation
from parse_zdump import timezone_rules, sortrules
from mpl_toolkits.axes_grid1 import make_axes_locatable

pd.set_option("display.max_rows", None, "display.max_columns", None)

states = geopandas.read_file('data/usa-states-census-2014.shp')

def plottzs(label=False, world=False, title=None,
            ruledata=None, possible_rules=None):
    # https://proj.org/
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_aspect('equal')

    gdf = geopandas.read_file('data/world/tz_world_mp.shp')
    gdf = gdf[~gdf['TZID'].str.contains('uninhabited')]  # don't plot Antartica
    gdf['coords'] = gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
    gdf['coords'] = [coords[0] for coords in gdf['coords']]

    # gdf = gdf.reset_index()
    gdf['rule'] = gdf.apply(lambda row: possible_rules.index(ruledata[row['TZID']]), axis=1)
    gdf['rule']=gdf['rule'].replace(0, np.NaN)
    gdf['nodst'] = gdf.apply(lambda row: possible_rules.index(ruledata[row['TZID']]), axis=1)
    # gdf['nodst']=gdf[gdf['nodst'] > 0.0] = np.NaN
    gdf['nodst'] = gdf['nodst'].apply(lambda x: x if x == 0 else np.NaN)

    if world:
        mill = pyproj.Proj(proj='robin', ellps='WGS84', datum='WGS84')
        gdf = gdf.to_crs(crs=mill.srs)
    else:  # CONUS
        mill = pyproj.Proj(proj='mill', ellps='WGS84', datum='WGS84')
        ax.set_xlim(-180, -50)
        ax.set_ylim(15, 75)

    cmap = plt.cm.get_cmap("brg").copy()
    cmap.set_bad(color='black', alpha=1.)
    vmin = gdf.rule.min()
    vmax = gdf.rule.max()
    my_mapi2 = gdf.plot(ax=ax, color='black', column='nodst', edgecolor='black')
    my_map = gdf.plot(ax=ax, cmap=cmap, column='rule', edgecolor='black')

    # label
    if label:
        for idx, row in gdf.iterrows():
            # print(row['TZID'], row['geometry'].area)
            if row['geometry'].area > 10:
                plt.annotate(s=row['TZID'].replace('America/', ''), xy=row['coords'],
                             horizontalalignment='center', color='white')
    ax.axis('off')
    if title is not None:
        plt.title(title, fontsize=20)

    divider = make_axes_locatable(ax)


    # color bar
    cax = divider.append_axes('bottom', size='5%', pad=0.05)
    data = np.arange(vmax, vmin, -1).reshape(1,int(vmax)-1)
    im = ax.imshow(data, cmap=cmap)
    cbar = fig.colorbar(im, cax=cax, orientation="horizontal", pad=0.2)
    cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])  # horizontal colorbar
    plt.show()


def visualize_dst_legislation():
    fig, ax = plt.subplots(figsize=(16, 9))
    #
    gdf = geopandas.read_file('data/cb_2018_us_state_20m.shp')
    aeqd = pyproj.Proj(proj='aeqd', ellps='WGS84', datum='WGS84', lat_0=39.0, lon_0=-98.5).srs
    df = df.to_crs(crs=aeqd)  # switch to mercator projection around US centroid

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
        tzs = []
        # tzs = pytz.country_timezones['US']
        tzs += pytz.country_timezones['CA']
        tzs = pytz.all_timezones
        import pickle
        try:
            fp = open("save.p", "rb")
            results_year_tz_rule = pickle.load(fp)
            fp.close()
            fp = open("save1.p", "rb")
            result = pickle.load(fp)
            fp.close()
            fp = open("save2.p", "rb")
            result2 = pickle.load(fp)
            fp.close()
        except:
            result, result2, results_year_tz_rule = timezone_rules(tzs, simplifyranges=False)
            pickle.dump(results_year_tz_rule, open("save.p", "wb"))
            pickle.dump(result, open("save1.p", "wb"))
            pickle.dump(result2, open("save2.p", "wb"))

        # pprint(results_year_tz_rule[2021])
        for year in range(2021,2022):
            rules = list(result.keys())
            rules=list(results_year_tz_rule[year].values())
            plottzs(ruledata=results_year_tz_rule[year], world=False,
                    label=True, possible_rules=sortrules(rules), title=year)

    def test_plot_CONUS_tz(self):
        plottzs()

    def test_plot_world_tz(self):
        plottzs(world=True)


if __name__ == '__main__':
    # visualize_dst_legislation()
    unittest.main()
