import re

from pytz import country_names
from new_app.libs.psql import db_clint
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from numpy import ndarray
from pandas import DataFrame

#FIRST MODUL

def data_reading(countries:list,skp:list): #returning filtered DataFrame with all skp and country product groups entered by the user (lists from Djobir)
    database = db_clint.read_sql()
    country_filter = database['country_name'].isin(countries)
    df_with_filter = database[country_filter]
    skp_filter = df_with_filter['skp'].isin(skp)
    df_with_filter = df_with_filter[skp_filter]
    return df_with_filter

def year(data:DataFrame): #func to know in which year we now
    return data['year_number'].unique()

def creating_duties(years:ndarray,data:DataFrame,skp:list): #creating skp groups duties
    columns = ['skp','value','year']
    duty = pd.DataFrame(columns=columns)
    for i in years:
        for j in skp:
            frame = data[(data['year_number'] == i) & (data['skp'] == j)]
            duty.loc[len(duty.index)] = [frame['skp'].unique(),frame['duty'].mean(),frame['year_number'].unique()]
    return duty

def creating_import(years:ndarray,data:DataFrame,skp:list): #creating skp groups import
    columns = ['skp','value','year']
    imp = pd.DataFrame(columns=columns)
    for i in years:
        for j in skp:
            frame = data[(data['year_number'] == i) & (data['skp'] == j)]
            imp.loc[len(imp.index)] = [frame['skp'].unique(),frame['price'].sum(),frame['year_number'].unique()]
    return imp

def elasticity_calculating(duty:DataFrame,imp:DataFrame,skp:list): #calculating elasticity for skp groups
    coef = np.empty((len(skp),2))
    elast = np.empty(len(skp))
    row = 0
    for i in skp:
        j = 0
        kol = 0
        x_frame = duty[duty['skp'] == i]
        y_frame = imp[imp['skp'] == i]
        for elem_x in x_frame['value']:
            if np.isnan(elem_x):
                kol+=1
        for elem_y in y_frame['value']:
            if np.isnan(elem_y):
                kol+=1
        if kol>0:
            coef[row,j]='NaN'
            j+=1
            coef[row,j]='NaN'
        else:
            x = x_frame['value'].values.reshape((-1,1))
            y = y_frame['value'].values
            x = np.log(x.astype('float'))
            y = np.log(y.astype('float'))
            model=LinearRegression().fit(x,y)
            coef[row,j]=model.intercept_
            j+=1
            coef[row,j]=model.coef_
        row += 1
    row = 0
    for i in skp:
        duty_frame = duty[duty['skp'] == i]
        imp_frame = imp[imp['skp'] == i]
        if not (np.isnan(coef[row,1])):
            elast[row] = coef[row,1]*(duty_frame['value'].mean()/imp_frame['value'].mean())
        else:
            elast[row] = 'NaN' # or NULL
        row += 1
    return elast

def adding_new_duties_to_df(data:DataFrame,products:list,duties:list): #developing (lists from Djobir)
    return

def adding_new_import(years:ndarray,skp:list,elasticity:ndarray,alpha:float,duty:DataFrame,imp:DataFrame): #import forecast for the new year
    j = 0
    for i in skp:
        new_duty = duty.loc[(duty['skp'] == i) & (duty['year'] == years[len(years)-1])]
        old_duty = duty.loc[(duty['skp'] == i) & (duty['year'] == years[len(years)-2])]
        old_import = imp.loc[(imp['skp'] == i) & (imp['year'] == years[len(years)-2])]
        imp.loc[(len(imp.index))] = [i,(1 + alpha + elasticity[j] * (new_duty['value'] - old_duty['value']))*old_import['value'],years[len(years)-1]]
        j += 1
    return imp


if __name__ == '__main__':
    country_id = ['Армения','Беларусь','Казахстан','Кыргызстан','Российская Федерация']
    skp = ['C13','C14','C15','C21','C29','C30']