# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/PretzelLogic
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


def getCol(title,list):
    return """<td><table class="pretzel list">
<tr><td colspan="2" class="title">
%s</td></tr>%s</table></td>"""%(title,list)


def getRow(name,value):
    return """<tr><td align=right class="name">%s</td>
<td class="value">%s</td></tr>"""%(name,value)


def getRetention(pas,fail,thold,hl): # a.k.a pass rate
    tr='n/a'; klass='tr_na'
    tot=pas+fail
    if tot and pas>=thold:
        perc=pas/float(tot)*100
        if perc>0:
            if pas>=hl:
                tr="%0.2f%%"%perc
                klass='tr_hot'
            else:
                tr="%0.1f%%"%perc
                klass='tr_cold'
    return '<span class="retention %s">%s</span>'%(klass,tr)


def getGradeFootNote(btn):
    if btn<2 or btn>4: return ""
    return """<div id="pretzel_footnote">
<span id="failed_grade_note"></span> <span 
id="failed_grade_msg"><span id="failed_grade" 
data-grade="%d"></span></span></div>"""%btn


def spanWrap(klass,val):
    return '<span class="%s">%d</span>'%(klass,val)
