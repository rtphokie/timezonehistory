# sources: KXTV https://www.abc10.com/article/news/nation-world/daylight-saving-time-bill-status-all-50-states/507-25ff8777-63bc-423f-895d-22f5a3d5d28c
# as of 2021-11
# 4 never observed 3 passed 2 pending 1 failed/stalled 0 no consideration
legislation = {
        'alabama':              3,
        'alaska':               2,
        'arizona':              4,
        'arkansas':             1,
        'california':           1,
        'colorado':             1,
        'connecticut':          1,
        'delaware':             3,
        'district of columbia': -1,
        'florida':              3,
        'georgia':              3,
        'hawaii':               4,
        'idaho':                3,
        'illinois':             2,
        'indiana':              -1,
        'iowa':                 2,
        'kansas':               1,
        'kentucky':             1,
        'louisiana':            3,
        'maine':                3,
        'maryland':             1,
        'massachusetts':        1,
        'michigan':             2,
        'minnesota':            3,
        'mississippi':          3,
        'missouri':             2,
        'montana':              3,
        'nebraska':             2,
        'nevada':               1,
        'new hampshire':        1,
        'new jersey':           2,
        'new mexico':           1,
        'new york':             1,
        'north carolina':       2,
        'north dakota':         1,
        'ohio':                 2,
        'oklahoma':             1,
        'oregon':               3,
        'pennsylvania':         2,
        'puerto rico':          -1,
        'rhode island':         -1,
        'south carolina':       3,
        'south dakota':         1,
        'tennessee':            3,
        'texas':                2,
        'utah':                 3,
        'vermont':              1,
        'virginia':             2,
        'washington':           3,
        'west virginia':        1,
        'wisconsin':            1,
        'wyoming':              3,
}

# listed here to enable some sorting
possible_rules = ['1st Sun in Jan - last Sun in Oct',
                  '1st Sun in Feb - last Sun in Oct',
                  '2nd Mon in Feb - 1st Sat in Jan',
                  '2nd Mon in Feb - 2nd Mon in Feb',
                  '2nd Mon in Feb - 2nd Tue in Aug',
                  'last Sun in Feb - last Sun in Oct',
                  '2nd Sun in Mar - 1st Sat in Jan',
                  '2nd Sun in Mar - 1st Sun in Nov',
                  'last Mon in Mar - last Sun in Oct',
                  'last Sun in Mar - 4th Sun in May',
                  'last Sun in Mar - last Sun in Oct',
                  'last Sun in Apr - 2nd Mon in Feb',
                  '2nd Sun in Apr - last Tue in May',
                  'last Sun in Apr - 3rd Sun in May',
                  'last Sun in Apr - 1st Sun in Jun',
                  'last Sun in Apr - 4th Sun in Jul',
                  'last Sun in Apr - last Wed in Aug',
                  '2nd Sun in Apr - 3rd Mon in Sep',
                  '4th Sun in Apr - 3rd Sat in Sep',
                  'last Sun in Apr - 1st Tue in Sep',
                  'last Sun in Apr - 4th Sun in Sep',
                  'last Sun in Apr - last Sun in Oct',
                  '1st Sat in Apr - 1st Sun in Oct',
                  '1st Sun in Apr - last Sun in Oct',
                  '2nd Sun in Apr - 1st Sun in Oct',
                  '2nd Sun in Apr - 2nd Sun in Oct',
                  '2nd Sun in Apr - last Sun in Oct',
                  'last Sun in Apr - 1st Mon in Oct',
                  'last Sun in Apr - 1st Sun in Oct',
                  'last Sun in Apr - 2nd Sun in Oct',
                  'last Sun in Apr - last Sun in Sep',
                  'last Sun in Apr - last Sun in Nov',
                  '1st Sun in May - 1st Sun in Oct',
                  '1st Sun in May - 1st Thu in Sep',
                  '1st Sun in May - 1st Tue in Sep',
                  '1st Sun in May - 3rd Mon in Sep',
                  '1st Sun in May - 3rd Sun in Sep',
                  '1st Sun in May - last Mon in Sep',
                  '1st Sun in May - last Sat in Sep',
                  '1st Sun in May - last Sun in Sep',
                  '1st Mon in May - last Sat in Sep',
                  '1st Mon in May - last Sun in Oct',
                  '1st Tue in May - 2nd Tue in Aug',
                  '1st Fri in May - 1st Mon in Sep',
                  '2nd Mon in May - 1st Mon in Oct',
                  '2nd Mon in May - 2nd Tue in Aug',
                  '2nd Mon in May - last Sun in Oct',
                  '2nd Sun in May - 1st Sun in Oct',
                  '2nd Sun in May - 1st Tue in Sep',
                  '2nd Sun in May - 2nd Sun in Oct',
                  '2nd Sun in May - 2nd Sun in Sep',
                  '2nd Sun in May - 3rd Mon in Sep',
                  '2nd Sun in May - 3rd Sun in Sep',
                  '2nd Sun in May - last Mon in Sep',
                  '2nd Sun in May - last Sun in Aug',
                  '3rd Mon in May - 1st Mon in Oct',
                  '3rd Sun in May - 2nd Mon in Sep',
                  '3rd Sun in May - 3rd Sat in Sep',
                  '3rd Sun in May - 3rd Sun in Sep',
                  '3rd Sun in May - 3rd Thu in Sep',
                  '3rd Sun in May - last Sun in Sep',
                  'last Sat in May - 4th Sat in Sep',
                  'last Sun in May - 1st Sat in Nov',
                  'last Sun in May - last Mon in Sep',
                  '1st Mon in Jun - 2nd Mon in Sep',
                  '1st Sun in Jun - 1st Sun in Sep',
                  '1st Sun in Jun - last Mon in Sep',
                  '2nd Sun in Jun - 2nd Sun in Sep',
                  '2nd Sun in Jun - last Sun in Oct',
                  '2nd Wed in Jun - last Sun in Oct',
                  '4th Sun in Jun - last Sun in Sep',
                  'last Fri in Jul - 2nd Tue in Aug',
                  '2nd Tue in Aug - last Sun in Sep',
                  'last Sun in Sep - 2nd Mon in Feb']