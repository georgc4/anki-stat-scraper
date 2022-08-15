# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all the Qt GUI library
from aqt.qt import *
import anki.cards
import anki.collection
from anki.consts import *
from anki.lang import FormatTimeSpan
from anki.utils import base62, ids2str
from anki import hooks
# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window

    cards, thetime, failed, lrn, rev, relrn, filt = mw.col.db.first(f"""
select count(), sum(time)/1000,
sum(case when ease = 1 then 1 else 0 end), /* failed */
sum(case when type = {REVLOG_LRN} then 1 else 0 end), /* learning */
sum(case when type = {REVLOG_REV} then 1 else 0 end), /* review */
sum(case when type = {REVLOG_RELRN} then 1 else 0 end), /* relearn */
sum(case when type = {REVLOG_CRAM} then 1 else 0 end) /* filter */
from revlog where id > ? """, (mw.col.sched.day_cutoff - 86400) * 1000,
        )
    # show a message box
    print (cards)
    #showInfo("Card count: %d" % cardCount)

# create a new menu item, "test"
action = QAction("Export Stats", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

