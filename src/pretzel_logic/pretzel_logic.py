# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/PretzelLogic
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import os, re
from aqt import mw
from anki.hooks import addHook

from .utils import *
from .stats import *
from .db import *
from .const import *

from .lib.com.lovac42.anki.backend.lang import getLang


class PretzelLogic:
    def __init__(self, conf):
        self.config = conf


    def getCutoff(self, days):
        return (mw.col.sched.dayCutoff-86400*days)*1000


    def setup(self, type, lim):
        self.mature_ivl=DEFAULT_MATURE_IVL
        self.type=type
        self.limit=" and "+lim if lim else ''
        self.olimit=self.limit #backup
        self.startDay=self.config.get('start_day_offset',0) or 0
        if self.startDay:
            span=self.getCutoff(self.startDay)
            self.limit=" and id <= %d%s"%(span,self.limit)

        self.view=self.config.get('display_mode','full')
        self.ease=self.config.get('failed_grade',
            DEFAULT_FAILED_GRADE) or 1
        self.threshold=self.config.get('pass_threshold',
            DEFAULT_PASS_THRESHOLD) or 20
        self.highlight=self.config.get('highlight_threshold',
            DEFAULT_HIGHLIGHT_THRESHOLD) or 100


    def getStyleSheet(self):
        lang=getLang() + ".css"
        fname=os.path.join("locale", lang)
        loc=self.config.readFile(fname, False)
        if not loc:
            fname=os.path.join('locale', 'en_US.css')
            loc=self.config.readFile(fname, False)
        fname=self.config.get('stylesheet', DEFAULT_STYLESHEET)
        css=self.config.readFile(fname, False)
        return """<style>%s %s</style>"""%(loc, css)


    def getFootNote(self):
        ftn=getGradeFootNote(self.ease)
        return FOOTNOTE_WARNING%(self.threshold,self.highlight,ftn)


    def getTimeframe(self):
        timeframe=self.config.get('timeframe',DEFAULT_TIMEFRAME)
        tf=timeframe[self.type] or DEFAULT_TIMEFRAME[self.type]
        arr=[]
        for days in sorted(tf):
            title=tf[days]
            if days=='inf':
                span=self.getCutoff(float(days))
            elif self.startDay:
                span=self.getCutoff(int(days)+self.startDay)
                title+='<span class="day_offset">%d</span>'%+self.startDay
            else:
                span=self.getCutoff(int(days))
            ilist=self.getIntervalList(span)
            arr.append(getCol(title,ilist))
        return arr


    def getIntervalList(self, span):
        geldMode=self.view=='classic'
        row=[]

        if geldMode: #Classic view
            g=getBowdlerizeSection(self.limit,span,
                self.ease,self.threshold,self.highlight)
            row.extend(g)
        else:
            quickMode=self.view=='quick'
            #Custom Range Between
            if not quickMode:
                crArr=self._getCustomRangeList(span)
                row.extend(crArr)
                row.extend('<tr><td colspan="2" class="hr"></td></tr>')

            #Young/Mature
            passed,flunked,ymArr=self._getMaturityList(span,quickMode)
            row.extend(ymArr)

            #Total:
            total=getTotalSection(self.limit,span,
                passed,flunked,self.threshold,self.highlight)
            row.extend(total)
        return "".join(row)


    def _getCustomRangeList(self,span):
        row=[]
        rIvls=self.config.get('custom_ivl_range_between',None)
        for ri in rIvls:
            fromIvl,toIvl=ri
            if fromIvl<=toIvl:
                ar,p,f=getRangeSection(self.limit,span,
                    self.ease,fromIvl,toIvl,self.threshold,self.highlight)
                row.extend(ar)
        return row


    def _getMaturityList(self,span,quickMode=False):
        row=[]
        ivls=self.config.get('interval_range') #if deleted
        ivls=ivls or (DEFAULT_MATURE_IVL,) #if empty or deleted
        for ivl in ivls:
            ar,pas,flk=getMatureSection(self.limit,span,ivl,
                    self.ease,self.threshold,self.highlight)
            if ivl==ivls[0]:
                self.mature_ivl=ivl
                passed_mature=pas
                flunked_mature=flk
                arr,passed_young,flunked_young=getYoungSection(self.limit,
                        span,ivl,self.ease,self.threshold,self.highlight)
                row.extend(arr)
            row.extend(ar)
            if quickMode: break
        passed=passed_young+passed_mature
        flunked=flunked_young+flunked_mature
        return passed,flunked,row


    def getCorrectionStats(self, stats):
        "Fix stats for total mature cards reviewed"
        span=self.getCutoff(1)
        ms=getMatureStats(self.olimit,span,self.mature_ivl,self.ease)
        arr=stats.split('<br>')
        if len(arr)<2: return stats #2.1 "no cards studied today"

        #Fix new/lrn count
        nCnt=getLearned(self.olimit,span)
        lCnt=getLearning(self.olimit,span)
        s=re.sub(r'\d+',str(lCnt),arr[-2],1)
        arr[-2]='<span id="newcnt">%d</span>'%nCnt + s

        #Fix mature stats for ease/mature ivl
        if ms:
            msg=arr[-1].split(':')
            arr[-1]=msg[0]+ms
        stats='<br>'.join(arr)

        #Add ReMemorize stats
        resched=getResched(self.olimit,span)
        if resched:
            stats+='<br><span id="resched" data-cnt="%d"></span>'%resched

        return '<div id="today_stats">'+stats+'''
<div class="tooltip"></div></div>'''
