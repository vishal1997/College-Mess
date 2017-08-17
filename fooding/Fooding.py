from fooding.breakfast import BreakFast
from fooding.lunch import Lunch
from fooding.dinner import Dinner
from fooding.snacks import Snacks
from fooding.demand import Demand
from fooding.select import Select
from fooding.bill import TotalBill



class Fooding:
    def breakfast(dateId):
        return BreakFast.breakfast(dateId)


    def lunch(dateId):
        return Lunch.lunch(dateId)
    
    def dinner(dateId):
        return Dinner.dinner(dateId)
    
    def snacks(dateId):
        return Snacks.snacks(dateId)

    def demand():
        return Demand.demand()

    def select():
        return Select.select()

    def bill():
        return TotalBill.bill()

    