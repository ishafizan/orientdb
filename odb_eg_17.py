# -*- coding: utf-8 -*-
import os
import sys
from json import dumps, loads
from time import sleep, time

try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    from util import util_gen
    from util import util_log
    from util import util_odb
except ImportError:
    raise Exception("import util files failed")

# -----------------------------
__author__ = 'Ishafizan'
__date__ = "2018-09-06"
# -----------------------------

log = util_log.logger()
start = time()
log.info("start: %s" % util_gen.getcurrdt())
log.info("*-" * 40)

# --------------------------------------
# QUERY via rest
# --------------------------------------

log.info("query: Find all Locations visited by Colin's friends")
query_str = "MATCH {Class: Profiles, as: profile, " \
            "where: (Name='Colin' and Surname='OrientDB')}" \
            "-HasFriend->{Class: Profiles, as: friend}<-HasProfile-{Class: Customers, as: customer}" \
            "-HasVisited->{Class: Locations, as: location} " \
            "RETURN location.@Rid as Location_RID, location.Name as Location_Name, " \
            "location.Type as Location_Type, friend.Name as Friend_Name, friend.Surname as Friend_Surname"
query_str = "MATCH {Class: Profiles, as: profile," \
            " where: (Name='Santo' and Surname='OrientDB')}" \
            "-HasFriend->{Class: Profiles, as: friend}" \
            "<-HasProfile-{Class: Customers, as: customer}" \
            "-HasVisited->{Class: Locations, as: location} " \
            "RETURN $pathelements"
log.info("---*" * 20)
res = util_odb.post_command(log, query_str)
log.info(dumps(res["result"]))

# -- END
end = time()
elapsed_time = end - start
log.info("*-" * 40)
log.info("time taken: %ss" % elapsed_time)
log.info("FINISH")
