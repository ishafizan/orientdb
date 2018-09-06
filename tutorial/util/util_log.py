# -*- coding: utf-8 -*-
import logging
import os.path
import sys

__author__ = 'Ishafizan'


# init logger
def logger():
    program = os.path.basename(sys.argv[0])
    log = logging.getLogger(program)
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.basicConfig(format='%(asctime)s : [%(filename)s:%(lineno)d] : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    log.info("running %s" % ' '.join(sys.argv))
    return log
