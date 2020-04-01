# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/PretzelLogic
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.utils import getText
from aqt.qt import *
from .const import *

from anki import version
ANKI21=version.startswith("2.1.")


class MenuItem:
    def __init__(self, config):
        self.config=config
        menu=None
        for a in mw.form.menubar.actions():
            if '&Study' == a.text():
                menu=a.menu()
                # menu.addSeparator()
                break
        if not menu:
            menu=mw.form.menubar.addMenu('&Study')

        qact=QAction(ADDON_NAME+": Show Stats", mw)
        qact.triggered.connect(self.showStats)
        menu.addAction(qact)


    def showStats(self):
        d=self.config.get('start_day_offset',0)
        day,ok=getText("Set starting day?", default=str(d))
        if not ok: return
        try:
            day=int(day)
        except ValueError: day=d
        self.config.set('start_day_offset',day)
        mw.onStats()
        self.config.set('start_day_offset',d)

