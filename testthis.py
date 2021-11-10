from mapit import plottzs
from pprint import pprint
import pickle
import pytz
import unittest
import numpy as np
from tqdm import tqdm
from datetime import datetime
from parse_zdump import timezone_rules, ordmonthday, listtoranges
from mapit import navajo_nation
from tzdatabase_parse import parse_rules_file


# /usr/share/zoneinfo

class MappingUnitTests(unittest.TestCase):
    def setUp(self):
        # speed up unit tests by not rerunning
        try:
            fp = open(f"IANA_tz_db_source_file_parsing_Tests.p", "rb")
            self.links, self.offset, self.rules = self.results_year_rule_tz = pickle.load(fp)
            fp.close()
            print('from cache')
        except Exception as e:
            print(e)
            self.links, self.offset, self.rules = parse_rules_file()
            fp = open(f"IANA_tz_db_source_file_parsing_Tests.p", "wb")
            pickle.dump((self.links, self.offset, self.rules), fp)
            fp.close()
            print("reparsed")

    def test_navajo_nation(self):
        navajo_nation()

    def test_us_rules(self):
        print(len(pytz.common_timezones))
        print(len(set(self.results_year_rule_tz[2021])))
        # pprint(sorted(set(self.results_year_rule_tz[2021])))
        # for rule in self.results_year_rule_tz[2021].keys():
        #     print(f"\n{rule}")
        #     pprint(self.results_year_rule_tz[2021][rule])
        #     print()
        for year in self.results_year_tz_codedrule.keys():
            print(year, self.results_year_tz_codedrule[year]['America/Denver'], self.results_year_tz_codedrule[year]['America/Boise'], )

    def test_metrics(self):
        rules = set()
        pprint(len(list(self.results_year_rule_tz[2021]['no DST'])))
        for year in self.results_year_rule_tz.keys():
            for rule in self.results_year_rule_tz[year].keys():
                rules.add(rule)
        print(len(rules))
        print(len(pytz.common_timezones))
        print(len(pytz.all_timezones))

    def test_tzs(self):
        for tz in ['US', 'CA', 'MX']:
            print(f'{tz} {len(pytz.country_timezones[tz])}')
            pprint(pytz.country_timezones[tz])
            pprint(pytz.country_timezones[tz])

        print(f"all {len(pytz.all_timezones)}")
        print(f"com {len(pytz.common_timezones)}")
        print(f"{set(pytz.all_timezones) - set(pytz.common_timezones)}")

    def test_plot_CONUS_tz_rules(self):
        # pprint(self.results_year_rule_tz[2021])
        pprint(self.results_year_tz_codedrule[2021])
        for year in range(2000, 2022):
            plottzs(ruledata=self.results_year_tz_codedrule[year],
                    world=False, label=True, title=year)

    def test_plot_world_tz_rules(self):
        # print(self.rules.keys())
        yearmapping={}
        for year in tqdm(range(1915, 2022)):
            yearmapping[year]={}
            for tz in self.rules.keys():
                # print(tz, list(self.rules[tz].keys()))
                if year in self.rules[tz].keys():
                    if 'dst' in self.rules[tz][year].keys():
                        yearmapping[year][tz]=self.rules[tz][year]['dst']['ord'][1]
            plottzs(ruledata=yearmapping[year], world=True, label=False, title=year)

    @unittest.skip("unneeded")
    def test_custom_colorbar(self):
        import matplotlib.pyplot as plt
        import matplotlib as mpl

        fig, ax = plt.subplots(figsize=(16, 9))
        fig.subplots_adjust(bottom=0.8)

        cmap = get_continuous_cmap(seasonal_hex_color_list)
        norm = mpl.colors.Normalize(vmin=0, vmax=13)

        cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='horizontal')
        cb1.set_label('Start of Daylight Saving')
        ticklabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        cb1.set_ticks(np.linspace(0, 12, len(ticklabels)))
        cb1.ax.tick_params(labelsize=25)
        cb1.ax.set_xticklabels(ticklabels)

        fig.show()


class IANA_tz_db_source_file_parsing_Tests(unittest.TestCase):
    def setUp(self):
        # speed up unit tests by not rerunning
        try:
            fp = open(f"IANA_tz_db_source_file_parsing_Tests.p", "rb")
            self.links, self.offset, self.rules = self.results_year_rule_tz = pickle.load(fp)
            fp.close()
            print('from cache')
        except Exception as e:
            print(e)
            self.links, self.offset, self.rules = parse_rules_file()
            fp = open(f"IANA_tz_db_source_file_parsing_Tests.p", "wb")
            pickle.dump((self.links, self.offset, self.rules), fp)
            fp.close()
            print("reparsed")

    def test_links(self):
        self.assertTrue('America/New_York' in self.links)
        self.assertTrue('America/Denver' in self.links)
        self.assertTrue('Europe/London' in self.links)
        self.assertTrue('UTC' in self.links)
        self.assertTrue('US/Eastern' in self.links['America/New_York'])

    def test_offset(self):
        self.assertTrue(1901, min(self.offset.keys()))
        self.assertTrue(2050, max(self.offset.keys()))

    def test_rules(self):
        self.assertGreaterEqual(9999, len(self.rules))
        self.assertTrue('America/New_York' in self.rules)
        self.assertTrue('America/Denver' in self.rules)
        self.assertTrue('Europe/London' in self.rules)
        pprint(self.rules['Africa/Abidjan'])
        pprint(self.rules['Pacific/Fiji'])


class ZDumpParsingUnitTests(unittest.TestCase):

    def test_us_timezones(self):
        tzs = pytz.country_timezones['US']
        # tzs += pytz.country_timezones['CA']
        timezone_rules(tzs)

    def testlist2ranges(self):
        thelist = [1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006]
        ranges = listtoranges(thelist)
        self.assertEqual(['1987-2006'], ranges)
        thelist = [1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006]
        ranges = listtoranges(thelist)
        self.assertEqual(['1987-1994', '1996-2006'], ranges)

    def testnth(self):
        foo, foo2 = ordmonthday(datetime(2021, 11, 7, 2))
        self.assertEqual(foo, '1st Sun in Nov 02:00:00')
        self.assertEqual(foo2, 11.010002)
