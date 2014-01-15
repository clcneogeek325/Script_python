#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

for x in range(21):
    tiempo = datetime.datetime.now()
    print "Son las i% con i% minutos y i% segundos" % (tiempo.hour,tiempo.minute,tiempo.second)
    time.sleep(1)
