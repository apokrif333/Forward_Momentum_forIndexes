import pandas as pd
import numpy as np
import os
import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import datetime

print("Enter max momentum from 1 to 12: ")
n_Momentum = 12#input()

#Функция корректировки даты
def DateCorrect(x):
    try:
        x["Date"] = pd.to_datetime(x["Date"])
    except:
        x["Date"] = pd.to_datetime(x["Date"], '%Y-%m-%d').date()

# Считываем файл, корректируем дату
SP_Base = pd.read_csv("S&P since 1870.csv", sep=",", encoding="latin-1")
DateCorrect(SP_Base)

year = relativedelta(years=1)
for u in range(1,n_Momentum+1):
    # Определяем стартовую и конечную дату
    StartDate = SP_Base["Date"][0]
    i = 0
    while SP_Base["Date"][i].year == SP_Base["Date"][i + 1].year:
        i += 1
    EndDate = SP_Base["Date"][i+1]

    Enter = []
    while len(Enter)<12:
       Enter.append(0)
    while len(Enter)<len(SP_Base["Date"]):
        StartDate = StartDate+year
        EndDate = EndDate+year
        TablePast = SP_Base.loc[(SP_Base["Date"]>=StartDate-year)&(SP_Base["Date"]<EndDate)]
        TableNow = SP_Base.loc[(SP_Base["Date"]>=StartDate+year)&(SP_Base["Date"]<EndDate+year)]
        for y in range(12,len(TablePast)):
            if TablePast["SP500"].iloc[y]>=TablePast["SP500"].iloc[y-u]:
                Enter.append(1)
            else:
                Enter.append(0)
            print(u)
            print(len(Enter))
            print(len(SP_Base["Date"]))

    SP_Base["Momentum "+str(u)] = Enter
SP_Base.to_csv("exportTables/SP_Window_"+"1"+".csv")