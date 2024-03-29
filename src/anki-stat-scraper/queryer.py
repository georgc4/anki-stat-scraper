from anki.consts import *
from datetime import timedelta, datetime
from aqt import mw
from anki.utils import ids2str
class Queryer:
    def get_cards(self):
        limit = ids2str([d["id"] for d in mw.col.decks.all()])
        db_hit= mw.col.db.first(
            f"""
        select
        sum(case when queue={QUEUE_TYPE_REV} and ivl >= 21 then 1 else 0 end), -- mtr
        sum(case when queue in ({QUEUE_TYPE_LRN},{QUEUE_TYPE_DAY_LEARN_RELEARN}) or (queue={QUEUE_TYPE_REV} and ivl < 21) then 1 else 0 end), -- yng/lrn
        sum(case when queue={QUEUE_TYPE_NEW} then 1 else 0 end), -- new
        sum(case when queue<{QUEUE_TYPE_NEW} then 1 else 0 end) -- susp
        from cards where did in %s"""
            % limit,
        )
        db_hit = [x if x is not None else 0 for x in db_hit]
        if db_hit:
            total = sum(db_hit)
            unlocked = total - db_hit[2]
            mature = db_hit[0]
            yng_lrn = db_hit[1]
            new = db_hit[2]
            susp = db_hit[3]
            return total, unlocked, mature, yng_lrn, new, susp
        else:
            return 0,0,0,0,0,0
    def get_hour_bkdwn(self):
        lim = ''
        if mw.col.sched_ver() == 1:
            sd = datetime.fromtimestamp(mw.col.crt)
            rolloverHour = sd.hour
        else:
            rolloverHour = mw.col.conf.get("rollover", 4)

        db_hit = mw.col.db.all(
            f"""
        select
        23 - ((cast((? - id/1000) / 3600.0 as int)) %% 24) as hour,
        sum(case when ease = 1 then 0 else 1 end) /
        cast(count() as float) * 100,
        count()
        from revlog where type in ({REVLOG_LRN},{REVLOG_REV},{REVLOG_RELRN}) %s
        group by hour having count() > 30 order by hour"""
            % lim,
            mw.col.sched.day_cutoff,
        )
        db_hit = [x if x is not None else 0 for x in db_hit]
        if db_hit:
            hours_dict = {(stat[0]+4) % 24 :stat[2] for stat in db_hit}
            return hours_dict
        else:
            return {}
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
        revs = [x if x is not None else 0 for x in revs]
        if revs:
            deltas = [rev[0] for rev in revs]
            cards = [sum(rev[1:5]) for rev in revs]
            times = [round(sum(rev[6:10]),3) for rev in revs]
            dates = [(today + timedelta(days=delta)).strftime("%Y_%m_%d") for delta in deltas]
            return dates, cards, times

        else:
            return [], [], []