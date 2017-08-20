from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataBase import Base, Student, History,Bill,BFMenu1,BFMenu2,BFMenu3,BFMenu4, Snack1,Snack2,NonVegItemLunch,NonVegItemDinner,VegItemLunch,VegItemDinner,BaseItemLunch,BaseItemDinner

def createDB():
    engine = create_engine('sqlite:///messmenu.db')
    Base.metadata.bind = engine
    DBsession = sessionmaker(bind=engine)
    db = DBsession()
    return db
