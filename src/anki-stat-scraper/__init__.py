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


    # def export_stats(self) -> None:
    #     # get the number of cards in the current collection, which is stored in
    #     # the main window
    #
    #     # client = pymongo.MongoClient(
    #     #     "mongodb+srv://cgeorges:<password>@cluster0.7txg8.mongodb.net/?retryWrites=true&w=majority")
    #     # db = client.test
    #     client = Client()

        # widget.set_output(str(json_doc))
    # create a new menu item, "test"
action = QAction("Export Stats 2", mw)
# set it to call testFunction when it's clicked
widget = Dialog()
qconnect(action.triggered, widget.exec)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
name,nshe = widget.name, widget.nshe
