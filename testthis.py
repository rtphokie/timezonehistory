import unittest
from pprint import pprint
import pytz
import pickle
from mapit import plottzs, timezone_rules


class MyMapping(unittest.TestCase):

    def setUp(self):
        # return results_rule_tz_years, results_year_rule_tz
        ver = 'all'

        tzs = []
        if ver == 'small':
            tzs += pytz.country_timezones['US']
            tzs += pytz.country_timezones['CA']
            tzs += pytz.country_timezones['MX']
        else:
            ver = 'all'
            tzs = pytz.all_timezones
        try:
            fp = open(f"results_year_rule_tz{ver}.p", "rb")
            self.results_year_rule_tz = pickle.load(fp)
            fp.close()
            fp = open(f"results_year_tz_codedrule{ver}.p", "rb")
            self.results_year_tz_codedrule = pickle.load(fp)
            fp.close()

        except:
            self.results_year_rule_tz, self.results_year_tz_codedrule = timezone_rules(tzs)
            fp = open(f"results_year_rule_tz{ver}.p", "wb")
            pickle.dump(self.results_year_rule_tz, fp)
            fp.close()
            fp = open(f"results_year_tz_codedrule{ver}.p", "wb")
            pickle.dump(self.results_year_tz_codedrule, fp)
            fp.close()

    def test_plot_CONUS_tz_rules(self):
        # pprint(self.results_year_rule_tz[2021])
        # pprint(self.results_year_tz_codedrule[2021])
        for year in range(2000, 2022):
            plottzs(ruledata=self.results_year_tz_codedrule[year],
                    world=False, label=True, title=year)

    def test_plot_world_tz_rules(self):
        for year in range(2021, 2022):
            plottzs(ruledata=self.results_year_tz_codedrule[year],
                    world=True, label=True, title=year)t

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


class tz_dump_tests(unittest.TestCase):

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

    def testparse(self):
        # 1965-04-25      02      -03     EDDT    1
        tzs = ['ACDT', 'ACST', 'ADDT', 'ADT', 'AEDT', 'AEST', 'AHDT', 'AHST', 'AKDT', 'AKST', 'AMT', 'APT', 'AST', 'AWDT', 'AWST', 'AWT', 'BDST', 'BDT', 'BMT',
               'BST', 'CAST', 'CAT', 'CDDT', 'CDT', 'CEMT', 'CEST', 'CET', 'CMT', 'CPT', 'CST', 'CWT', 'ChST', 'DMT', 'EAT', 'EDDT', 'EDT', 'EEST', 'EET',
               'EMT', 'EPT', 'EST', 'EWT', 'FFMT', 'FMT', 'GDT', 'GMT', 'GST', 'HDT', 'HKST', 'HKT', 'HKWT', 'HMT', 'HPT', 'HST', 'HWT', 'IDDT', 'IDT', 'IMT',
               'IST', 'JDT', 'JMT', 'JST', 'KDT', 'KMT', 'KST', 'LMT', 'LST', 'MDDT', 'MDST', 'MDT', 'MEST', 'MET', 'MMT', 'MPT', 'MSD', 'MSK', 'MST', 'MWT',
               'NDDT', 'NDT', 'NPT', 'NST', 'NWT', 'NZDT', 'NZMT', 'NZST', 'PDDT', 'PDT', 'PKST', 'PKT', 'PLMT', 'PMMT', 'PMT', 'PPMT', 'PPT', 'PST', 'PWT',
               'QMT', 'RMT', 'SAST', 'SDMT', 'SET', 'SJMT', 'SMT', 'SST', 'TBMT', 'TMT', 'UTC', 'WAST', 'WAT', 'WEMT', 'WEST', 'WET', 'WIB', 'WIT', 'WITA',
               'WMT', 'YDDT', 'YDT', 'YPT', 'YST', 'YWT', ]

        prob = []
        for tz in tzs:
            datestr = f'Mon Feb 9 01:59:59 1942 {tz}'
            try:
                dt = arrow.get(f'{datestr.strip()}', 'MMM D hh:mm:ss YYYY ZZZ')
                prob.append(tz)
            except:
                pass
        pprint(prob)
