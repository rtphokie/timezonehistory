import datetime
from tqdm import tqdm
import unittest
from pprint import pprint
import subprocess
import pytz
import re
import arrow
import math
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta


def ordmonthday(dt):
    ''' determine the ordinal weekday of a given datetime (e.g. first Sunday in November)
    :param dt: datetime
    :return: string of the form <ordinal 1st, 2nd, ... last> <day of the week> in <month>
    '''
    words = ['ERROR', '1st', '2nd', '3rd', '4th', 'last']
    first_day = dt.replace(day=1)
    last_day = (first_day + relativedelta(months=+1)).replace(day=1) - timedelta(days=1)
    day = dt.day
    ord = math.ceil(day / 7)

    if (last_day.day - dt.day) < 7:
        ords = 'last'
    else:
        ords = words[ord]
    #         self.assertEqual(foo2, '11.000702')
    s = f"{ords} {dt.strftime('%a in %b %H:%M')}"
    coded = float(f"{dt.strftime('%m')}.{words.index(ords):02}{dt.strftime('%w')}{dt.strftime('%w')}{dt.strftime('%H')}")
    return s, coded


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


def timezone_rules(tzs):
    '''
    Note: this code assumes DST starts and stops within the same calendar year which
          does not well handle "War Time" during WWII (1942-1945) in North America which spanned 1942-1945
    :param tzs: list of timezone strings
    :return: dictionaries:
             DST rules, the timezones that use them, and the years they were in effect
    '''
    zdump_re_pattern = '.*UTC = ([\w\s:]+) ([\w\+\-]+) isdst=(\d)'  # note, zdump output varies slightly by OS, this is the format seen on Macs (BSD)
    date_str_pattern = 'MMM D hh:mm:ss YYYY'
    results_year_rule_tz = {}
    results_year_codedrule_tz = {}
    results_year_tz_codedrule = {}
    # tzs=['America/New_York', 'America/Phoenix', 'America/Los_Angeles']
    # tzs = ['America/Phoenix']
    for tz in tqdm(tzs):
        # for tz in tqdm(tzs):
        result = subprocess.run(['zdump', '-v', '-c', '2022', tz], stdout=subprocess.PIPE)
        lines = result.stdout.decode('utf-8').split("\n")

        r0 = re.match(zdump_re_pattern, lines[0])
        dt0 = arrow.get(r0.group(1), date_str_pattern)  # arrow/dateutil don't reliably parse abbreviated time zone names
        r1 = re.match(zdump_re_pattern, lines[-2])  # compensate for trailing CR
        dt1 = arrow.get(r1.group(1), date_str_pattern)  # arrow/dateutil don't reliably parse abbreviated time zone names
        all_years = list(range(int(dt0.year), int(dt1.year) + 1))
        for year in all_years:
            if year not in results_year_rule_tz.keys():
                results_year_rule_tz[year] = {'no DST': []}
                results_year_codedrule_tz[year] = {0.0: []}
                results_year_tz_codedrule[year] = {}

        prevdt = None
        prev_isdst = 0
        # dst_start=None
        # dst_end=None
        for line in lines[:-2]:
            r = re.match(zdump_re_pattern, line)
            if r:
                datestr = r.group(1).strip().replace('  ', ' ')
                tzabbr = r.group(2)
                isdst = int(r.group(3))

                dt = arrow.get(datestr, date_str_pattern)  # arrow/dateutil don't reliably parse abbreviated time zone names

                if prev_isdst != isdst:  # rules change
                    if isdst == 1:  # observe DST
                        dst_start = prevdt.shift(seconds=1)
                    elif isdst == 0:  # back to standard time
                        dst_end = prevdt + timedelta(seconds=1)
                        rulestr = f"{ordmonthday(dst_start)[0]} - {ordmonthday(dst_end)[0]}"
                        rulecode = ordmonthday(dst_start)[1]
                        if rulestr not in results_year_rule_tz[dt.year].keys():
                            results_year_rule_tz[dt.year][rulestr] = []
                        for year in range(dst_start.year, dst_end.year + 1):
                            if rulestr not in results_year_rule_tz[year].keys():
                                results_year_rule_tz[year][rulestr] = []
                                results_year_codedrule_tz[year][rulecode] = []
                            if rulecode not in results_year_codedrule_tz[year].keys():
                                results_year_codedrule_tz[year][rulecode] = []
                            results_year_rule_tz[year][rulestr].append(tz)
                            results_year_codedrule_tz[year][rulecode].append(tz)
                            results_year_tz_codedrule[year][tz] = rulecode
                    else:
                        raise ValueError(f"unexpected DST flag {isdst} {line}")
                prevdt = dt
                prev_isdst = isdst

            else:
                raise ValueError(line)

        # fill in years with no DST rules
        for year in all_years:
            found = False
            for rule in results_year_rule_tz[year].keys():
                found = found or tz in results_year_rule_tz[year][rule]
            if not found:
                results_year_rule_tz[year]['no DST'].append(tz)
                results_year_codedrule_tz[year][0.0].append(tz)
                results_year_tz_codedrule[year][tz] = 0.0

    return results_year_rule_tz, results_year_tz_codedrule


if __name__ == '__main__':
    unittest.main()
