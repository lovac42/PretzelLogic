# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/PretzelLogic
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from aqt.utils import getText
from anki.hooks import addHook

from .const import ADDON_NAME
from .lib.com.lovac42.anki.gui import toolbar


class MenuItem:
    _loaded = False

    def __init__(self, config):
        self.config = config
        addHook(ADDON_NAME+".configLoaded", self.setupMenu)


    def setupMenu(self):
        if self._loaded:
            return
        self._loaded = True

        m_name = self.config.get("menu_name", "&Study")
        menu = toolbar.getMenu(mw, m_name)

        qact = QAction(ADDON_NAME+": Show Stats", mw)
        qact.triggered.connect(self.showStats)
        menu.addAction(qact)


    def showStats(self):
        d=self.config.get('start_day_offset', 0)
        day,ok=getText("Set starting day?", default=str(d))
        if not ok:
            return

        try:
            day = int(day)
        except ValueError:
            day = d

        self.config.set('start_day_offset', day)
        mw.onStats()
        self.config.set('start_day_offset', d)

