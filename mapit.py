from data import legislation
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tqdm import tqdm
import geopandas
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import pyproj

pd.set_option("display.max_rows", None, "display.max_columns", None)

seasonal_hex_color_list = ['#06b4cf', '#1acf06', '#cccf06', '#cf8506', '#061acf']


# states = geopandas.read_file('data/usa-states-census-2014.shp')

def get_continuous_cmap(hex_list, float_list=None):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list.

        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.

        Returns
        ----------
        colour map
        via https://towardsdatascience.com/beautiful-custom-colormaps-with-matplotlib-5bab3d1f0e72
        '''
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0, 1, len(rgb_list)))

    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = mcolors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp


def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values'''
    value = value.strip("#")  # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values'''
    return [v / 256 for v in value]


def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    seq = list(seq)
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)


def plottzs(label=False, world=False, title=None,
            ruledata=None, possible_rules=None):
    # https://proj.org/
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_aspect('equal')

    gdf = geopandas.read_file('data/world/tz_world_mp.shp')
    gdf = gdf[~gdf['TZID'].str.contains('uninhabited')]  # don't plot Antartica
    gdf['coords'] = gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
    gdf['coords'] = [coords[0] for coords in gdf['coords']]

    for tz in list(gdf['TZID']):
        if tz not in ruledata.keys():
            raise ValueError(f"{tz} not in")

    gdf['rule'] = gdf.apply(lambda row: ruledata[row['TZID']], axis=1)
    gdf['nodst'] = gdf['rule'].copy()
    gdf['rule'] = gdf['rule'].replace(0.0, np.NaN)
    gdf['nodst'] = gdf['nodst'].apply(lambda x: x if x == 0.0 else np.NaN)

    if world:
        mill = pyproj.Proj(proj='robin', ellps='WGS84', datum='WGS84')
        gdf = gdf.to_crs(crs=mill.srs)
    else:  # CONUS
        mill = pyproj.Proj(proj='mill', ellps='WGS84', datum='WGS84')
        ax.set_xlim(-180, -50)
        ax.set_ylim(15, 75)

    cmap = get_continuous_cmap(seasonal_hex_color_list)
    cmap_black = get_continuous_cmap(seasonal_hex_color_list)

    cmap.set_bad(color='black', alpha=1.)
    my_map = gdf.plot(ax=ax, cmap=cmap, column='rule', edgecolor='black')
    my_mapi2 = gdf.plot(ax=my_map, cmap=plt.get_cmap('gist_earth'), column='nodst', edgecolor='black')

    # label
    if label:
        for idx, row in gdf.iterrows():
            if row['geometry'].area > 10:
                plt.text(s=row['TZID'].replace('America/', ''),
                         x=row['coords'][0], y=row['coords'][1],
                         horizontalalignment='center', color='white')
    if title is not None:
        plt.title(title, fontsize=20)

    divider = make_axes_locatable(ax)

    # # color bar
    if not world:
        cax = divider.append_axes('bottom', size='5%', pad=0.05)
        data = np.arange(0, 13, 1).reshape(1, 13)
        im = ax.imshow(data, cmap=cmap)
        norm = mpl.colors.Normalize(vmin=1, vmax=13)
        cbar = fig.colorbar(im, cax=cax, orientation="horizontal", pad=0.2)
        ticklabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        cbar.set_ticks(np.linspace(0, 12, len(ticklabels)))  # start at 0 (Jan 1) end at 13 (Jan 1 following year)
        cbar.ax.set_xticklabels(ticklabels)  # horizontal colorbar

    ax.set_axis_off()
    plt.tight_layout()
    if world:
        plt.savefig(f'world_{title:04}.png', dpi=600)
    else:
        plt.savefig(f'north_america_{title:04}.png', dpi=600)


    # plt.show()


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


if __name__ == '__main__':
    # visualize_dst_legislation()
    fp = open(f"results_year_tz_codedruleall.p", "rb")
    results_year_tz_codedrule = pickle.load(fp)
    fp.close()
    for year in tqdm(range(1915, 2022)):
        plottzs(ruledata=results_year_tz_codedrule[year],
                world=False, label=False, title=year)