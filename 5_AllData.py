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

WindowL = []
CAGR = []
StDev = []
DrawDown = []
Sharpe = []
MaR = []
SM = []

for Window in range(1, 89):
    BaseFile = pd.read_csv("exportTables_SPX/Window_"+str(Window)+"_Capital"+".csv", sep=",", encoding="latin-1")
    DateCorrect(BaseFile)

    WindowL.append(Window)
    CAGR.append(((BaseFile["Capital"].iloc[-1]/BaseFile["Capital"].iloc[0])**
                 (1/(BaseFile["Date"].iloc[-1].year+1-BaseFile["Date"].iloc[0].year))-1)*100)
    StDev.append(stat.stdev(BaseFile["MonthCng"])*math.sqrt(12))
    DrawDown.append(min(BaseFile["DrawDown"]))
    Sharpe.append(CAGR[Window-1] / StDev[Window-1])
    MaR.append(abs(CAGR[Window-1] / (DrawDown[Window-1]*100)))
    SM.append(Sharpe[Window-1]*MaR[Window-1])

exportTable = pd.DataFrame({"Window": WindowL,
                               "CAGR": CAGR,
                               "StDev": StDev,
                               "DrawDown": DrawDown,
                               "Sharpe": Sharpe,
                               "MaR": MaR,
                               "SM": SM},
                              columns=["Window","CAGR","StDev","DrawDown","Sharpe","MaR","SM"]
                              )

exportTable.to_csv("exportTables_SPX/AllWindows_Data" + ".csv")