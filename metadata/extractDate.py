#!/usr/bin/env python
# coding: utf-8

import datetime
# import re
from typing import List

import schluesselregex as rex


def datumConv(day, month, year):

    monate = {
        'Januar': '01',
        'Februar': '02',
        'März': '03',
        'April': '04',
        'Mai': '05',
        'Juni': '06',
        'Juli': '07',
        'August': '08',
        'September': '09',
        'Oktober': '10',
        'November': '11',
        'Dezember': '12',
        'Jan': '01',
        'Feb': '02',
        'Mär': '03',
        'Apr': '04',
        'Mai': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sept': '09',
        'Okt': '10',
        'Nov': '11',
        'Dez': '12'
    }

    if month in monate.keys():
        month = monate[month]

    if len(year) == 2:
        if int(year) > 21:
            year = '19' + year  # 19XX
        else:
            year = '20' + year  # 20XX

    try:
        dt = datetime.datetime(year=int(year), month=int(month), day=int(day))
    except:
        dt = datetime.datetime(year=1000, month=1, day=1)

    return dt  # , timestamp


def getDates(text: str) -> List[datetime.datetime]:
    """
    Parses dates from a supplied `text` string and returns them as a list of datetimes.
    If no dates are found, returns a [datetime.datetime(year=1000, month=1, day=1)] list.

    :param str text: The string to parse for dates
    :return list: A list of datetime formatted dates
    """
    date_dmy = rex.getRegex(text).datum_dmy
    date_ymd = rex.getRegex(text).datum_ymd

    dtList = []
    # timestampList = []

    if text == '':
        return dtList

    if date_dmy:
        # day month year found --> (' ', '16', '.', 'Februar', ' ', '2011')
        for i in date_dmy:
            day = i[1]
            month = i[3]
            year = i[5]

            dt = datumConv(day, month, year)
            dtList.append(dt)

    if date_ymd:
        # year month day found --> (' ', '2011', '-', '02', '-', '17')
        for i in date_ymd:
            year = i[1]
            month = i[3]
            day = i[5]

            dt = datumConv(day, month, year)
            dtList.append(dt)

    if dtList:
        if max(dtList) - min(dtList) > datetime.timedelta(days=365*10):
            dtList.remove(min(dtList))

        dtList = list(set(dtList))
    else:
        dtList = [datetime.datetime(year=1000, month=1, day=1)]

    return dtList
