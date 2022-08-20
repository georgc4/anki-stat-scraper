from anki.consts import *
from datetime import timedelta, datetime
from aqt import mw

class Queryer:
    def get_cards(self):
        return mw.col.db.first(
            f"""
        select
        sum(case when queue={QUEUE_TYPE_REV} and ivl >= 21 then 1 else 0 end), -- mtr
        sum(case when queue in ({QUEUE_TYPE_LRN},{QUEUE_TYPE_DAY_LEARN_RELEARN}) or (queue={QUEUE_TYPE_REV} and ivl < 21) then 1 else 0 end), -- yng/lrn
        sum(case when queue={QUEUE_TYPE_NEW} then 1 else 0 end), -- new
        sum(case when queue<{QUEUE_TYPE_NEW} then 1 else 0 end) -- susp
        from cards where did in %s"""
            % mw._limit()
        )
    def get_revs(self):
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
        times = [round(sum(rev[6:10]),3) for rev in revs]
        dates = [(today + timedelta(days=delta)).strftime("%Y_%m_%d") for delta in deltas]
        return dates, cards, times
