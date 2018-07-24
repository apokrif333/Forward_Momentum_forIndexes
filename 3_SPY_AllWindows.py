import pandas as pd
import numpy as np
import os
import datetime as dt
import statistics as stat
import math
from dateutil.relativedelta import relativedelta
from datetime import datetime

#Функция корректировки даты
def DateCorrect(x):
    try:
        x["Date"] = pd.to_datetime(x["Date"])
    except:
        x["Date"] = pd.to_datetime(x["Date"], '%Y-%m-%d').date()

# Считываем файл, корректируем дату
BaseFile = pd.read_csv("exportTables_SPX/SP_AllCapital.csv", sep=",", encoding="latin-1")
DateCorrect(BaseFile)

year = relativedelta(years=1)
for Window in range(1, BaseFile["Date"].iloc[-1].year-BaseFile["Date"].iloc[0].year): #
    exportTable = pd.DataFrame({})

    StartDate = BaseFile["Date"][0]
    i = 0
    while BaseFile["Date"][i].year == BaseFile["Date"][i + 1].year:
        i += 1
    EndDate = BaseFile["Date"][i + 1]

    for u in range (0, BaseFile["Date"].iloc[-1].year-BaseFile["Date"].iloc[0].year-2):
        if EndDate.year-StartDate.year == Window:
            StartDate = StartDate + year
            EndDate = EndDate + year
            TablePast = BaseFile.loc[(BaseFile["Date"] >= StartDate) & (BaseFile["Date"] <= EndDate)]
        else:
            EndDate = EndDate + year
            TablePast = BaseFile.loc[(BaseFile["Date"] >= StartDate) & (BaseFile["Date"] <= EndDate)]

        TableFuture = BaseFile.loc[(BaseFile["Date"] >= EndDate) & (BaseFile["Date"] < EndDate+year)]
        Sharpe = []
        BestMoment = []
        print(EndDate)

        for i in range(1, 13):
            StDev = stat.stdev(TablePast["MonthCng "+str(i)])*math.sqrt(12)
            CAGR = ((TablePast["Capital "+str(i)].iloc[-1]/TablePast["Capital "+str(i)].iloc[0])**(1/(EndDate.year-StartDate.year ))-1)*100
            if StDev != 0:
                Sharpe.append(round(CAGR/StDev,3))
            else:
                Sharpe.append(0)

        for i in range(0, 12):
            BestMoment.append(Sharpe.index(max(Sharpe))+1)

        curExportTable = pd.DataFrame({"Date": TableFuture["Date"],
                                       "Close": TableFuture["Close"],
                                       "Dividend": TableFuture["Dividend"],
                                       "MomentumType": BestMoment,
                                       "Enter": TableFuture["Momentum "+str(BestMoment[0])]},
                                      columns=["Date","Close","Dividend","MomentumType","Enter"]
                                      )

        exportTable = pd.concat([exportTable, curExportTable], ignore_index=True)

    exportTable.to_csv("exportTables_SPX/Window_" + str(Window)+ ".csv")
    print("exportTables_SPX/Window_" + str(Window)+ ".csv")