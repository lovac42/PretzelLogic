# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/PretzelLogic
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1

# performance info:
# https://www.sqlite.org/np1queryprob.html

from aqt import mw

# REVLOG TYPES:
#    0=lrn (new)
#    1=rev (review)
#    2=relrn (lapsed)
#    3=early review (filtered)
#    4=scheduled (ReMemorize)

def getRelearned(lim, span):
    return getLearned(lim,span,type=2)

def getLearned(lim, span, type=0):
    return mw.col.db.first("""Select
sum(case when type = ? and ivl > 0 then 1 else 0 end)
from revlog where id > ? %s"""%lim,type,span)[0] or 0

def getFlunkedLessThan(lim, span, toIvl, ease):
    return mw.col.db.first("""Select
sum(case when ease <= ? and type = 1 and
lastIvl > 0 and lastIvl < ? then 1 else 0 end)
from revlog where id > ? %s"""%lim,ease,toIvl,span)[0] or 0

def getPassedLessThan(lim, span, toIvl, ease):
    return mw.col.db.first("""Select
sum(case when ease > ? and type = 1 and
lastIvl > 0 and lastIvl < ? then 1 else 0 end)
from revlog where id > ? %s"""%lim,ease,toIvl,span)[0] or 0

def getFlunkedGreaterThan(lim, span, toIvl, ease):
    return mw.col.db.first("""Select
sum(case when ease <= ? and type = 1 and
lastIvl >= ? then 1 else 0 end)
from revlog where id > ? %s"""%lim,ease,toIvl,span)[0] or 0

def getPassedGreaterThan(lim, span, toIvl, ease):
    return mw.col.db.first("""Select
sum(case when ease > ? and type = 1 and
lastIvl >= ? then 1 else 0 end)
from revlog where id > ? %s"""%lim,ease,toIvl,span)[0] or 0

def getFlunkedRange(lim, span, ease, fromIvl, toIvl):
    return mw.col.db.first("""Select
sum(case when ease <= ? and type = 1 and
lastIvl >= ? and lastIvl <= ? then 1 else 0 end)
from revlog where id > ? %s"""%lim,ease,fromIvl,toIvl,span)[0] or 0

def getPassedRange(lim, span, ease, fromIvl, toIvl):
    return mw.col.db.first("""Select
sum(case when ease > ? and type = 1 and
lastIvl >= ? and lastIvl <= ? then 1 else 0 end)
from revlog where id > ? %s"""%lim,ease,fromIvl,toIvl,span)[0] or 0

def getResched(lim, span):
    return mw.col.db.first("""Select
sum(case when type = 4 and ease = 0 then 1 else 0 end)   /* ReMemorize */
from revlog where id > ? %s"""%lim,span)[0] or 0
