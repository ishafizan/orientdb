# -*- coding: utf-8 -*-
import os
import sys
import pyorient
import requests
from time import time, sleep
from json import dumps, loads

try:
    from pyorient.types import OrientBinaryObject, OrientRecordLink
except ImportError:
    from pyorient.otypes import OrientBinaryObject, OrientRecordLink

try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    import settings
    from util import util_gen
except ImportError:
    raise Exception("import util files failed")

# -----------------------------------
# utility functions for orientdb
__author__ = 'Ishafizan'
__date__ = "2018-09-06"


# -----------------------------------
# Generic post command
# -----------------------------------
def post_command(log, query):
    try:
        search_start = time()
        payload = {"command": query}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        l = requests.Session().post(
            'http://%s:%s/command/%s/sql/' % (
                settings.ORIENTDB_TARGET, settings.ORIENTDB_API_PORT, settings.ORIENTDB_DB_NAME),
            data=dumps(payload), headers=headers, auth=(settings.ORIENTDB_DB_USR, settings.ORIENTDB_DB_PWD))
        # log.info(l)
        resp_dict = loads(l.content)
        log.info("search results: %s" % len(resp_dict["result"]))

        search_end = time()
        util_gen.display_elapsed_time(log, "post_command", search_start, search_end)

        return resp_dict
    except Exception as error:
        log.error(error)
