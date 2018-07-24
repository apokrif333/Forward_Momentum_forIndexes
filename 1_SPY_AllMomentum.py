import pandas as pd
import numpy as np
import os
import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import datetime

n_Momentum = 12

#Функция корректировки даты
def DateCorrect(x):
    try:
        x["Date"] = pd.to_datetime(x["Date"])
    except:
        x["Date"] = pd.to_datetime(x["Date"], '%Y-%m-%d').date()

# Считываем файл, корректируем дату
SP_Base = pd.read_csv("SPXMonthly.csv", sep=",", encoding="latin-1")
DateCorrect(SP_Base)

year = relativedelta(years=1)
#Перебираем моментумы
for u in range(1,n_Momentum+1):
    # Определяем стартовую и конечную дату
    StartDate = SP_Base["Date"][0]
    i = 0
    while SP_Base["Date"][i].year == SP_Base["Date"][i+1].year:
        i += 1
    EndDate = SP_Base["Date"][i+1]

    #Заполняем Enter, чтобы его массив был равен массиву SP_Base.
    Enter = []
    while len(Enter)<12:
       Enter.append(0)

    #Создаём окно с данными текущего года и прошлого
    while len(Enter) < len(SP_Base["Date"]):
        StartDate = StartDate+year
        EndDate = EndDate+year

        TablePast = SP_Base.loc[(SP_Base["Date"] >= StartDate-year) & (SP_Base["Date"] < EndDate)]
        print(len(TablePast))
        #Перебираем все месяцы в текущем году по моментуму
        for y in range(12, len(TablePast)):
            if TablePast["Close"].iloc[y] >= TablePast["Close"].iloc[y-u]:
                Enter.append(1)
            else:
                Enter.append(0)

            print(u)
            print(len(Enter))

    #Когда посчитали данный моментум по всей истории, создать столбик в SP_Base
    SP_Base["Momentum "+str(u)] = Enter
#Создать файл со всеми моментумами для текущего окна
SP_Base.to_csv("exportTables_SPX/SP_AllMomentum"+".csv")