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

log.info("query: Find Colin's friends who are also Customers")
query_str = "MATCH {Class: Profiles, as: profile," \
            " where: (Name='Santo' AND Surname='OrientDB')}" \
            "-HasFriend-{Class: Profiles, as:friend}<-HasProfile" \
            "-{class:Customers, as: customer} " \
            "RETURN $pathelements"

query_str = "MATCH {Class: Profiles, as: profile," \
            " where: (Name='Santo' AND Surname='OrientDB')}" \
            "-HasFriend-{Class: Profiles, as:friend}<-HasProfile" \
            "-{class:Customers, as: customer} " \
            "RETURN friend.@Rid as Friend_RID, friend.Name as Friend_Name, " \
            "friend.Surname as Friend_Surname, " \
            "customer.@Rid as Customer_RID, " \
            "customer.OrderedId as Customer_OrederedId"


log.info("---*" * 20)
res = util_odb.post_command(log, query_str)
log.info(dumps(res["result"]))

# -- END
end = time()
elapsed_time = end - start
log.info("*-" * 40)
log.info("time taken: %ss" % elapsed_time)
log.info("FINISH")
