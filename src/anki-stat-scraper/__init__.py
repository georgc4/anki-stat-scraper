# import the main window object (mw) from aqt
# import pymongo
from aqt import mw
import aqt.stats
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
from .client import Client
# import all the Qt GUI library
from aqt.qt import *
from .dialog import Dialog
import anki.cards
import json
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


def on_click():
    widget = Dialog()
    widget.exec()
action = QAction("Export Stats 2", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, on_click)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
