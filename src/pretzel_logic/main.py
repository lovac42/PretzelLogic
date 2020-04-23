# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/PretzelLogic
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# Credits:
# Idea based on "True Retention" - Strider  
# https://ankiweb.net/shared/info/613684242

# Look and feel influenced by "True Retention by Card Maturity" - Glutanimate  
# https://ankiweb.net/shared/info/923360400

# Some credit should be attributed to Damien Elmes for the original methods leading to this development.

# Note: This addon is not built upon the aforementioned works, but a complete rewrite with those ideas included and licensed under GNU GPL, version 3 or later. There is no fuzz on authorship here.


import anki.stats
from anki.hooks import wrap

from .const import ADDON_NAME
from .config import *
from .pretzel_logic import *
from .menuitem import *


conf = Config(ADDON_NAME)
pl = PretzelLogic(conf)
mi = MenuItem(conf)


def todayStats(stat, _old):
    lim = stat._revlogLimit()
    pl.setup(stat.type,lim)
    tf=pl.getTimeframe() #call first
    s=pl.getCorrectionStats(_old(stat)) #call after
    css=pl.getStyleSheet()
    ftNote=pl.getFootNote()
    return s+css+"""<br><br><div id="pretzel_logic">
<table style='text-align:center'><tr>%s</tr>
</table>%s</div>"""%(''.join(tf),ftNote)

anki.stats.CollectionStats.todayStats=wrap(anki.stats.CollectionStats.todayStats, todayStats, 'around')

