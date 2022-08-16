# import the main window object (mw) from aqt
import pymongo
from aqt import mw
import aqt.stats
from pprint import pprint
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all the Qt GUI library
from aqt.qt import *
import anki.cards
from datetime import datetime
from datetime import timedelta
import anki.collection
from anki.consts import *
from anki import stats
from anki.lang import FormatTimeSpan
from anki.utils import base62, ids2str
from anki import hooks
# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
def get_cards():
    return self.col.db.first(
        f"""
    select
    sum(case when queue={QUEUE_TYPE_REV} and ivl >= 21 then 1 else 0 end), -- mtr
    sum(case when queue in ({QUEUE_TYPE_LRN},{QUEUE_TYPE_DAY_LEARN_RELEARN}) or (queue={QUEUE_TYPE_REV} and ivl < 21) then 1 else 0 end), -- yng/lrn
    sum(case when queue={QUEUE_TYPE_NEW} then 1 else 0 end), -- new
    sum(case when queue<{QUEUE_TYPE_NEW} then 1 else 0 end) -- susp
    from cards where did in %s"""
        % self._limit()
    )
def get_revs():
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    revs = mw.col.db.all(
        f"""
        select
        (cast((id/1000.0 - ?) / 86400.0 as int))/? as day,
        sum(case when type = {REVLOG_LRN} then 1 else 0 end), -- lrn count
        sum(case when type = {REVLOG_REV} and lastIvl < 21 then 1 else 0 end), -- yng count
        sum(case when type = {REVLOG_REV} and lastIvl >= 21 then 1 else 0 end), -- mtr count
        sum(case when type = {REVLOG_RELRN} then 1 else 0 end), -- lapse count
        sum(case when type = {REVLOG_CRAM} then 1 else 0 end), -- cram count
        sum(case when type = {REVLOG_LRN} then time/1000.0 else 0 end)/?, -- lrn time
        -- yng + mtr time
        sum(case when type = {REVLOG_REV} and lastIvl < 21 then time/1000.0 else 0 end)/?,
        sum(case when type = {REVLOG_REV} and lastIvl >= 21 then time/1000.0 else 0 end)/?,
        sum(case when type = {REVLOG_RELRN} then time/1000.0 else 0 end)/?, -- lapse time
        sum(case when type = {REVLOG_CRAM} then time/1000.0 else 0 end)/? -- cram time
        from revlog %s
        group by day order by day"""
        % '',
        mw.col.sched.day_cutoff,
        1,
        1,
        1,
        1,
        1,
        1,
    )
    deltas = [rev[0] for rev in revs]
    cards = [sum(rev[1:5]) for rev in revs]
    times = [sum(rev[6:10]) for rev in revs]
    dates = [(today + timedelta(days=delta)).strftime("%Y_%m_%d") for delta in deltas]
    return dates, cards, times

    pprint(revs)
def export_stats() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window

    # client = pymongo.MongoClient(
    #     "mongodb+srv://cgeorges:<password>@cluster0.7txg8.mongodb.net/?retryWrites=true&w=majority")
    # db = client.test
    dates, cards, times = get_revs()



# create a new menu item, "test"
action = QAction("Export Stats", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, export_stats)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

