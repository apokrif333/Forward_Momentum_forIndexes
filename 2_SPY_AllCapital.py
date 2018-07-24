import pandas as pd
import numpy as np
import os
import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import datetime

StartCapital = 10000
DivMonth = [3, 6, 9, 12]

#Функция корректировки даты
def DateCorrect(x):
    try:
        x["Date"] = pd.to_datetime(x["Date"])
    except:
        x["Date"] = pd.to_datetime(x["Date"], '%Y-%m-%d').date()

# Считываем файл, корректируем дату
BaseFile = pd.read_csv("exportTables_SPX/SP_AllMomentum.csv", sep=",", encoding="latin-1")
DateCorrect(BaseFile)

for i in range(1, 13):
    Columns = BaseFile.columns
    Capital = []
    Shares = []
    MonthCng = []

    for u in range(0, len(BaseFile["Date"])):
        QuartDiv = (BaseFile["Dividend"][u]/BaseFile["Close"][u]/4+1)
        if u == 0:
            Shares.append(0)
            Capital.append(StartCapital)
            MonthCng.append(0)

        elif BaseFile["Momentum "+str(i)][u-1] == 0 and BaseFile["Momentum "+str(i)][u] == 1:
            if BaseFile["Date"][u].month in (DivMonth):
                Shares.append(Capital[-1]/BaseFile["Close"][u]*QuartDiv)
            else:
                Shares.append(Capital[u-1]/BaseFile["Close"][u])
            Capital.append(Capital[-1])

        elif BaseFile["Momentum "+str(i)][u-1] == 1 and BaseFile["Momentum "+str(i)][u] == 1:
            if BaseFile["Date"][u].month in (DivMonth):
                Shares.append(Shares[-1]*QuartDiv)
            else:
                Shares.append(Shares[-1])
            Capital.append(Shares[u]*BaseFile["Close"][u])

        elif BaseFile["Momentum "+str(i)][u-1] == 1 and BaseFile["Momentum "+str(i)][u] == 0:
            Shares.append(0)
            Capital.append(Shares[u-1]*BaseFile["Close"][u])

        elif BaseFile["Momentum "+str(i)][u-1] == 0 and BaseFile["Momentum "+str(i)][u] == 0:
            Shares.append(0)
            Capital.append(Capital[-1])

        if u > 0:
            MonthCng.append(round((Capital[u]/Capital[u-1]-1)*100,2))

    BaseFile.insert(loc=Columns.get_loc("Momentum "+str(i))+1, column="Shares "+str(i), value=Shares)
    BaseFile.insert(loc=Columns.get_loc("Momentum "+str(i))+2, column="Capital "+str(i), value=Capital)
    BaseFile.insert(loc=Columns.get_loc("Momentum "+str(i))+3, column="MonthCng "+str(i), value=MonthCng)

BaseFile.to_csv("exportTables_SPX/SP_AllCapital"+".csv")