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

for Window in range(1,146):
    BaseFile = pd.read_csv("exportTables_SPX/Window_"+str(Window)+".csv", sep=",", encoding="latin-1")
    DateCorrect(BaseFile)

    Columns = BaseFile.columns
    Capital = []
    Shares = []
    MonthCng = []
    Down = []
    High = 0

    for u in range(0, len(BaseFile["Date"])):
        QuartDiv = (BaseFile["Dividend"][u] / BaseFile["Close"][u] / 4 + 1)
        if u == 0 and BaseFile["Enter"][0] == 1:
            Shares.append(StartCapital/BaseFile["Close"][0])
            Capital.append(StartCapital)
            MonthCng.append(0)

        elif u == 0 and BaseFile["Enter"][0] == 0:
            Shares.append(0)
            Capital.append(StartCapital)
            MonthCng.append(0)

        elif BaseFile["Enter"][u - 1] == 0 and BaseFile["Enter"][u] == 1:
            if BaseFile["Date"][u].month in (DivMonth):
                Shares.append(Capital[-1] / BaseFile["Close"][u] * QuartDiv)
            else:
                Shares.append(Capital[u - 1] / BaseFile["Close"][u])
            Capital.append(Capital[-1])

        elif BaseFile["Enter"][u - 1] == 1 and BaseFile["Enter"][u] == 1:
            if BaseFile["Date"][u].month in (DivMonth):
                Shares.append(Shares[-1] * QuartDiv)
            else:
                Shares.append(Shares[-1])
            Capital.append(Shares[u] * BaseFile["Close"][u])

        elif BaseFile["Enter"][u - 1] == 1 and BaseFile["Enter"][u] == 0:
            Shares.append(0)
            Capital.append(Shares[u - 1] * BaseFile["Close"][u])

        elif BaseFile["Enter"][u - 1] == 0 and BaseFile["Enter"][u] == 0:
            Shares.append(0)
            Capital.append(Capital[-1])

        if u > 0:
            MonthCng.append(round((Capital[u] / Capital[u - 1] - 1) * 100, 2))
        if Capital[u]>High:
            High = Capital[u]
        Down.append(Capital[u]/High-1)


    BaseFile.insert(loc=Columns.get_loc("Enter")+1, column="Shares", value=Shares)
    BaseFile.insert(loc=Columns.get_loc("Enter")+2, column="Capital", value=Capital)
    BaseFile.insert(loc=Columns.get_loc("Enter")+3, column="MonthCng", value=MonthCng)
    BaseFile.insert(loc=Columns.get_loc("Enter")+4, column="DrawDown", value=Down)

    BaseFile.to_csv("exportTables_SPX/Window_" + str(Window)+"_Capital" + ".csv")