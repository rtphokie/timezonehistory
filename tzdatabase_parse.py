from pprint import pprint
import arrow
import re
import math
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from tqdm import tqdm

pattern_zone = 'TZ="([\_\-\/\w]+)"'
pattern_link = 'Link\s+([+\/\w]+)\s+([_\/\w]+)'
pattern_offset = '-\s-\s+([+\-])([+\-\d]+)\s*(\w*)'
pattern_rule = '([\d\-]+)\s+\d+'
pattern_skip = '^[#R]'


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
    s = f"{ords} {dt.strftime('%a in %b %H:%M')}"
    coded = float(f"{dt.strftime('%m')}.{words.index(ords):02}{dt.strftime('%w')}{dt.strftime('%w')}{dt.strftime('%H')}")
    return s, coded


def parse_rules_file(filename='tzdb-2021e/to2050.tzs'):
    fp = open(filename, 'r')
    lines = fp.readlines()
    fp.close()
    links = {}
    rules = {}
    offset = {}
    tz = None
    for line in tqdm(lines, desc='parsing rules'):
        line = line.strip()
        if re.match(pattern_skip, line):
            continue

        rL = re.match(pattern_link, line)
        rT = re.match(pattern_zone, line)
        ro = re.match(pattern_offset, line)
        rr = re.match(pattern_rule, line)
        if rL:
            for x in [(1, 2), (2, 1)]:
                if rL.group(x[0]) not in links.keys():
                    links[rL.group(x[0])] = []
                links[rL.group(x[0])].append(rL.group(x[1]))
        elif ro:
            # format: - -   +/-HHMMSS offset from UTC
            sign = ro.group(1)
            timestring = ro.group(2)

            for i in range(0, len(timestring), 2):
                offset[tz][int(i / 2)] = int(timestring[i:i + 2])
            if sign == '-':
                offset[tz][0] *= -1
            offset[tz][3] = offset[tz][0] * 60 ** 2
            offset[tz][3] += offset[tz][1] * 60
            offset[tz][3] += offset[tz][2]
        elif rr:
            if '/' not in tz:
                continue
            # 1916-06-15      00      +01     WEST    1
            atoms = line.split("\t")
            dst = atoms[-1] == '1'
            while len(atoms[1]) < 8:
                atoms[1] += ':00'  # pad assumed minutes and seconds
            newoffset = [0, 0, 0]  # hours minutes seconds
            for c in range(1, len(atoms[2]), 2):
                newoffset[int((c - 1) / 2)] = atoms[2][c:c + 2]
            if atoms[2][0] == '-':
                newoffset[0] *= -1
            dt = arrow.get(f"{atoms[0]} {atoms[1]}", 'YYYY-MM-DD hh:mm:ss')
            if len(atoms) == 5:
                rules[tz][dt.year] = {'dst': {'dt':   dt, 'offset': atoms[2], 'utc_offset': newoffset, 'abbrev': atoms[3] if len(atoms) >= 4 else None,
                                              'line': line, 'ord': ordmonthday(dt), 'dst': dst}}
            else:
                if prevyear not in rules[tz]:
                    prevyear = dt.year
                    rules[tz][prevyear] = {'st': {}}
                rules[tz][prevyear]['st'] = {'dt':   dt, 'offset': atoms[2], 'utc_offset': newoffset, 'abbrev': atoms[3] if len(atoms) >= 4 else None,
                                             'line': line, 'ord': ordmonthday(dt), 'dst': dst}
            prevyear = dt.year
        elif rT:
            tz = rT.group(1).strip()
            prevyear = None
            offset[tz] = [0, 0, 0, 0]  # hours, minutes, seconds, total seconds
            rules[tz] = {}

    return links, offset, rules
