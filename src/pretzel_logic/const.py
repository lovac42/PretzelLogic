# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/PretzelLogic
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from anki import version
ANKI21=version.startswith("2.1.")

ADDON_NAME='PretzelLogic'

DEFAULT_FAILED_GRADE=1

DEFAULT_PASS_THRESHOLD=20

DEFAULT_HIGHLIGHT_THRESHOLD=100

DEFAULT_MATURE_IVL=21

SUPER_MATURE_IVL=100

DEFAULT_TIMEFRAME=(
    { # type = 0
        "001": "Today:",
        "007": "Past week:",
        "031": "Past month:"
    },
    { # type = 1
        "001": "Today:",
        "007": "Past week:",
        "365": "Past year:"
    },
    { # type = 2
        "001": "Today:",
        "007": "Past week:",
        "inf": "All time:"
    }
)

DEFAULT_LOCALE='en_US'

DEFAULT_STYLESHEET="default.css"

TRUE_RETENTION='<span class="retention"></span>'

SUPER_MATURE='<span class="supermature"></span>'

PASSED_REVIEWS='<span class="passed"></span>'

FLUNKED_REVIEWS='<span class="flunked"></span>'

NEW_CARDS_REVIEWS='<span class="newcard"></span>'

LAPSED_REVIEWS='<span class="lapsed"></span>'

RESCHED_REVIEWS='<span class="resched"></span>'

FOOTNOTE_WARNING="""<div class="pretzel footnote">
<span id="passed_min" data-min="%d"></span><br />
<span id="passed_max" data-max="%d"></span><br />
%s</div>"""
