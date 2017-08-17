
from foodinghistory.history import History
from foodinghistory.bfHistory import BfHistory
from foodinghistory.dnHistory import DnHistory
from foodinghistory.lnHistory import LnHistory
from foodinghistory.snHistory import SnHistory


class FoodingHistory:
    def history():
        return History.history()

    def bfHistory(dateId):
        return BfHistory.bfHistory(dateId)

    def lnHistory(dateId):
        return LnHistory.lnHistory(dateId)

    def dnHistory(dateId):
        return DnHistory.dnHistory(dateId)

    def snHistory(dateId):
        return SnHistory.snHistory(dateId)