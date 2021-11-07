import datetime
from tqdm import tqdm
import unittest
from pprint import pprint
import subprocess
import pytz
import re
import arrow
import math
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def ordmonthday(dt):
    ''' determine the ordinal weekday of a given datetime (e.g. first Sunday in November)
    :param dt: datetime
    :return: string of the form <ordinal 1st, 2nd, ... last> <day of the week> in <month>
    '''
    words = ['ERROR', '1st', '2nd', '3rd', '4th']
    first_day = dt.replace(day=1)
    last_day = (first_day + relativedelta(months=+1)).replace(day=1) - timedelta(days=1)
    day = dt.day
    ord = math.ceil(day / 7)

    if (last_day.day - dt.day) < 7:
        ords = 'last'
    else:
        ords = words[ord]
    return f"{ords} {dt.strftime('%a in %b')}"


def listtoranges(thelist):
    '''reduces list of integers to list of ranges. For improved readbility of lists of years
       e.g.:
       [2010, 2011, 2012] -> ['2010-2012']
       [2010, 2011, 2012, 2014] -> ['2010-2012', '2014]
    :param thelist: list of integers
    :return:
    '''
    l = thelist.copy()
    sorted(l)
    prev = None
    result = [str(l[0])]
    lastpos = False
    for i, x in enumerate(l):
        if prev is not None and x != prev + 1:
            result[len(result) - 1] += f"-{prev}"
            result.append(str(x))
            if i == len(l):
                lastpos = True
        prev = x
    if not lastpos and len(l) > 1:
        result[len(result) - 1] += f"-{prev}"
    return result

def sortrules(rulestrings):
    '''
    sorts a list of rules of the form ordinal dow in month - ordinal dow in month
    e.g. 1st Mon in Jan - last Sun in Mar

    :param rulestrings: list of rules
    :return: sorted list of rules
    '''
    tmp = {}
    dow = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for x in list(rulestrings): # build dictionary with keys that are more sortable
        print(x)
        atoms = x.split(' ')
        if 'DST' not in x:
            tmp[f"{months.index(atoms[3]):02} {atoms[0][0]} {dow.index(atoms[1]):02}  {months.index(atoms[8]):02} {atoms[5][0]} {dow.index(atoms[6]):02} "] = x
    result = ['no DST']
    for key in sorted(tmp):
        result.append(tmp[key])
    return result

def timezone_rules(tzs, simplifyranges=True):
    '''

    :param tzs: list of timezone strings
    :return: dictionaries:
             DST rules, the timezones that use them, and the years they were in effect
    '''
    zdump_re_pattern = '([\w\/-]+) [\w\s:]+ UTC = ([\w\s:]+) (\d+) ([\w\+-]+) isdst=(\d)'
    results_rule_tz_years = {'no DST': {}}
    results_year_rule_tz = {}
    years=[]

    for tz in tqdm(tzs):
        result = subprocess.run(['zdump', '-v', '-c', '2022', tz], stdout=subprocess.PIPE)
        lines = result.stdout.decode('utf-8').split("\n")
        r0 = re.match(zdump_re_pattern, lines[0])
        r1 = re.match(zdump_re_pattern, lines[-2])

        if r0 is None:
            continue
        firstyear = int(r0.group(3))
        lastyear = int(r1.group(3))

        allyears = list(range(firstyear, lastyear + 1))
        results_rule_tz_years['no DST'][tz] = allyears
        for year in allyears:
            if year not in results_year_rule_tz.keys():
                results_year_rule_tz[year]={'no DST': []}
            results_year_rule_tz[year]['no DST'].append(tz)


        # pattern is the lines of isdst=1, isdst=1, isdst=0.  Cal date in first line is the beginning of DST, Cal date of third line is the end.
        prevdst = None
        prevdate = None

        for line in lines:
            r = re.match(zdump_re_pattern, line)
            if r:
                date = r.group(2)[4:]
                year = int(r.group(3))
                dst = int(r.group(5))
                years.append(year)

                dt = arrow.get(f'{year} {date} {tz}'.replace('  ', ' '), 'YYYY MMM D h:m:s ZZZ').shift(seconds=+1)
                if dst:
                    dt = dt.shift(seconds=+1)
                if dst == 1 and prevdst == 1:
                    s = f'{ordmonthday(prevdt)} - {ordmonthday(dt)}'

                    # results_rule_tz_years
                    if s not in results_rule_tz_years.keys():
                        results_rule_tz_years[s] = {}
                    if tz not in results_rule_tz_years[s].keys():
                        results_rule_tz_years[s][tz] = []
                    results_rule_tz_years[s][tz].append(year)
                    if year in results_rule_tz_years['no DST'][tz]:
                        results_rule_tz_years['no DST'][tz].remove(year)
                    if tz in results_year_rule_tz[year]['no DST']:
                        results_year_rule_tz[year]['no DST'].remove(tz)

                    # results_rule_tz_years
                    if year not in results_year_rule_tz.keys():
                        results_year_rule_tz[year] = {}
                    if s not in results_year_rule_tz[year].keys():
                        results_year_rule_tz[year][s] = []
                    results_year_rule_tz[year][s].append(tz)

                prevdst = dst
                prevdate = date
                prevdt = dt

    if simplifyranges:
        # simplify year lists to ranges
        for rule in results_rule_tz_years.keys():
            for tzstr in results_rule_tz_years[rule].keys():
                results_rule_tz_years[rule][tzstr] = listtoranges(results_rule_tz_years[rule][tzstr])

    results_year_tz_rule = {}
    for year in range(min(years), max(years)+1):
        results_year_tz_rule[year]={}
        for tz in tzs:
            if tz not in results_year_tz_rule[year].keys():
                results_year_tz_rule[year][tz]='No DST'
    for rule in results_rule_tz_years.keys():
        for tz in results_rule_tz_years[rule].keys():
            for year in results_rule_tz_years[rule][tz]:
                results_year_tz_rule[year][tz] = rule

    return results_rule_tz_years, results_year_rule_tz


class MyTestCase(unittest.TestCase):

    def test_us_timezones(self):
        tzs = pytz.country_timezones['US']
        # tzs += pytz.country_timezones['CA']
        results_rule_tz_years, results_year_rule_tz, = timezone_rules(tzs, simplifyranges=False)
        pprint(list(result.keys()))

    def testlist2ranges(self):
        thelist = [1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006]
        ranges = listtoranges(thelist)
        self.assertEqual(['1987-2006'], ranges)
        thelist = [1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006]
        ranges = listtoranges(thelist)
        self.assertEqual(['1987-1994', '1996-2006'], ranges)

    def testnth(self):
        foo = ordmonthday(datetime(2021, 11, 7))
        self.assertEqual(foo, '1st Sun in Nov')


if __name__ == '__main__':
    unittest.main()
