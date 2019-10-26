# -*- coding: utf-8 -*-
import datetime

def time_br(time):
    end_time = str(time)[:-6]
    if (end_time.count('.') == 0):
        end_time += '.000000'
    d = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    FULL_MONTHS = {1:'janeiro',  2:'fevereiro', 3:u'março',4:'abril', 5:'maio', 6:'junho', 7:'julho', 8:'agosto', 9:'setembro', 10:'outubro',  11:'novembro', 12:'dezembro'}
    return u"%s de %s às %s:%s" % (d.day,FULL_MONTHS[d.month],d.hour,d.minute)