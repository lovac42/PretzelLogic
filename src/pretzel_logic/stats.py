# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/PretzelLogic
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


from aqt import mw
from .utils import *
from .db import *
from .const import *


def getMatureStats(lim, span, matureIvl, ease):
    mcnt, msum, resched = mw.col.db.first("""select count(),
sum(case when type < 4 and ease > ? then 1 else 0 end),  /* passed */
sum(case when type = 4 and ease = 0 then 1 else 0 end)   /* ReMemorize */
from revlog where lastIvl >= ? and id > ?"""+lim,ease,matureIvl,span)
    if resched:
        ret=u': 0'
        mcnt-=resched #offset matured ReMemorize rescheduled counts
        if mcnt:
            msum=msum or 0
            return u": %(a)d/%(b)d (%(c).1f%%)" % dict(
                a=msum, b=mcnt, c=(msum / float(mcnt) * 100))


def getYoungSection(lim, span, ivl, ease, thold, hl):
    p=getPassedLessThan(lim,span,ivl,ease)
    f=getFlunkedLessThan(lim,span,ivl,ease)
    tr=getRetention(p,f,thold,hl)
    r=[]
    r.append(u"""<tr><td colspan="2" class="section young">
<span class="title" data-ivl="%d"></span></td></tr>"""%ivl)
    r.append( getRow(TRUE_RETENTION, tr) ) #already wrapped
    r.append( getRow(PASSED_REVIEWS, spanWrap("passed",p)) )
    r.append( getRow(FLUNKED_REVIEWS,spanWrap("flunked",f)) )
    return r,p,f


def getMatureSection(lim, span, ivl, ease, thold, hl):
    p=getPassedGreaterThan(lim,span,ivl,ease)
    f=getFlunkedGreaterThan(lim,span,ivl,ease)
    tr=getRetention(p,f,thold,hl)
    r=[]
    r.append(u"""<tr><td colspan="2" class="section mature">
<span class="title" data-ivl="%d"></span></td></tr>"""%ivl)
    r.append( getRow(TRUE_RETENTION, tr) )
    r.append( getRow(PASSED_REVIEWS, spanWrap("passed",p)) )
    r.append( getRow(FLUNKED_REVIEWS,spanWrap("flunked",f)) )
    return r,p,f


def getBowdlerizeSection(lim, span, ease, thold, hl):
    p=getPassedGreaterThan(lim,span,1,ease) # gt or eq
    f=getFlunkedGreaterThan(lim,span,1,ease)
    r=getTotalSection(lim,span,p,f,thold,hl)
    p=getPassedGreaterThan(lim,span,SUPER_MATURE_IVL,ease)
    f=getFlunkedGreaterThan(lim,span,SUPER_MATURE_IVL,ease)
    tr=getRetention(p,f,thold,hl)
    r[0]=r[1]
    r[1]=getRow(SUPER_MATURE,tr)
    return r


def getTotalSection(lim, span, passed, flunked, thold, hl):
    tr=getRetention(passed,flunked,thold,hl)
    lrn=getLearned(lim,span)
    relrn=getRelearned(lim,span)
    resched=getResched(lim,span)
    r=[]
    r.append(u"""<tr><td colspan="2" class="section total">
<span class="title"></span></td></tr>""")
    r.append( getRow(TRUE_RETENTION, tr) )
    r.append( getRow(PASSED_REVIEWS, spanWrap("passed",passed)) )
    r.append( getRow(FLUNKED_REVIEWS,spanWrap("flunked",flunked)) )
    r.append( getRow(NEW_CARDS_REVIEWS,spanWrap("newcard",lrn)) )
    r.append( getRow(LAPSED_REVIEWS, spanWrap("lapsed",relrn)) )
    r.append( getRow(RESCHED_REVIEWS, spanWrap("resched",resched)) )
    return r


def getRangeSection(lim, span, ease, fromIvl, toIvl, thold, hl):
    p=getPassedRange(lim,span,ease,fromIvl,toIvl)
    f=getFlunkedRange(lim,span,ease,fromIvl,toIvl)
    tr=getRetention(p,f,thold,hl)
    r=[]
    r.append(u"""<tr><td colspan="2" class="section range">
<span class="title" data-from="%d" data-to="%d">
</span></td></tr>"""%(fromIvl,toIvl))
    r.append( getRow(TRUE_RETENTION, tr) ) #already wrapped
    r.append( getRow(PASSED_REVIEWS, spanWrap("passed",p)) )
    r.append( getRow(FLUNKED_REVIEWS,spanWrap("flunked",f)) )
    return r,p,f
