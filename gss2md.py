import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime
from dateutil.parser import parse

import math

scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'cred.json', scope)

gc = gspread.authorize(credentials)
ws = gc.open("2019-02")

lst_seet = ws.worksheets()

lst_out = []
for seet in lst_seet:
    list_of_lists = seet.get_all_values()
    if 0 == len(list_of_lists):
        continue

    lst_format = []
    h_last = -1
    cnt = 0
    for row in list_of_lists:
        ymdhms = parse(row[0])

        if 0 != ymdhms.hour - h_last:
            lst_format.append('## {}月{}日 {}時'.format(ymdhms.month, ymdhms.day, ymdhms.hour))
            h_last = ymdhms.hour

        name = row[1]
        msg = row[2]
        lst_format.append("{:<10}「{}」".format(name, msg))
        if 0 < len(lst_format) - 1000: # about
            lst_out.append(lst_format)
            lst_format = []
            h_last = -1
            d_last = -1
            cnt = 0

    lst_out.append(lst_format)


cnt = 0
for out in lst_out:
    with open('out/out_%i.txt' % cnt, mode='w') as f:
        write_msg = "\n".join(out)
        f.write(write_msg)

    cnt += 1

