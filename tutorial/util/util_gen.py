# -*- coding: utf-8 -*-
import settings
import sys
import getopt
import urllib.parse as quote_plus
from datetime import datetime, date, timedelta
from time import strptime, mktime, sleep
from random import randint
from re import findall, compile

__author__ = 'Ishafizan'


# -------------------------------
def get_keywords_upgrade(log, keyword):
    keyword = quote_plus(keyword)
    return keyword


word_re = compile("\w+")


def _cap(match):
    return match.group(0).capitalize()


def capitalize_all(s):
    return word_re.sub(_cap, s)


def get_text_length(text):
    text_length = len(findall(r'\b\w+\b', text))
    text_length_cat = get_text_length_category(text_length)
    return text_length, text_length_cat


# get category
def get_text_length_category(msg_len):
    msg_len = int(msg_len)
    if msg_len <= 10:
        length_category = " below 10 words"
    elif 10 < msg_len <= 50:
        length_category = " between 10 to 50 words"
    elif 50 < msg_len <= 100:
        length_category = " between 50 to 100 words"
    elif 100 < msg_len <= 500:
        length_category = " between 100 to 500 words"
    elif 500 < msg_len <= 1000:
        length_category = " between 500 to 1000 words"
    elif msg_len > 1000:
        length_category = " above 1000 words"
    else:
        length_category = " unknown"
    return length_category


# -------------------------------
# TIME MANIPULATION
# -------------------------------
# get current time
def getcurrdt():
    dt = datetime.now()
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt


def get_sleep_time(one, two):
    timer = randint(one, two)
    return timer


def display_elapsed_time(log, msg, start, end):
    elapsed_time = end - start
    log.info("%s: %s seconds" % (msg, elapsed_time))


# get current time yyyy-mm-dd
def getcurrdt_yyyymmdd():
    dt = datetime.now()
    dt = dt.strftime("%Y-%m-%d")
    return dt


# string into datetime
def strtodt(mydt):
    mydt = strptime(mydt, "%Y-%m-%d %H:%M:%S")
    return mydt


# -- twitter specific
def formatdtiso(created_time):
    time_struct = strptime(created_time, '%a %b %d %H:%M:%S +0000 %Y')
    strdate = datetime.fromtimestamp(mktime(time_struct))
    return strdate


# operation timerange allowed
def ops_dt(log, currdt):
    # get YYYY-MM-DD
    ymd = getcurrdt_yyyymmdd()
    # change info datetime with start-end datetime
    pme = strtodt("%s %s" % (ymd, "23:59:59"))
    pms = strtodt("%s %s" % (ymd, "10:00:00"))

    if pms <= currdt <= pme:
        log.info("*" * 100)
        log.info("Operation in sleep timerange")
        # sleep for 8 hours
        log.info("Sleep for 8 hours")
        log.info("*" * 100)
        sleep(8 * 60 * 60)

    else:
        log.info("*" * 100)
        log.info("Operation NOT in sleep timerange")
        log.info("*" * 100)
