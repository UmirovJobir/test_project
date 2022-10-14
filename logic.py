
from new_app.libs.psql import db_clint
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from numpy import ndarray, product
from pandas import DataFrame


def elast_modul(countries:list,skp:list):
    pass
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
    columns = ['skp','value','year_number']
    duty = pd.DataFrame(columns=columns)
    for i in years:
        for j in skp:
            frame = data[(data['year_number'] == i) & (data['skp'] == j)]
            duty.loc[len(duty.index)] = [frame['skp'].unique(),frame['duty'].mean(),frame['year_number'].unique()]
    return duty

def creating_import(years:ndarray,data:DataFrame,skp:list): #creating skp groups import
    columns = ['skp','value','year_number']
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

def adding_new_duties_to_df(data:DataFrame,products:list,duties:list,years:ndarray): #adding new duties from user to DF (lists from Djobir)
    new_duties = data[data['year_number'] == years[-2]]
    new_duties.set_index('product_name',drop=False,inplace=True)
    j = 0
    for i in products:
        new_duties.loc[i,'duty'] = duties[j]
        j += 1
    new_duties.reset_index(drop=True,inplace=False)
    new_duties.loc[:,'year_number'] = years[-1]
    data = pd.concat([data,new_duties])
    return data

def adding_new_import(years:ndarray,skp:list,elasticity:ndarray,alpha:float,duty:DataFrame,imp:DataFrame): #import forecast for the new year
    j = 0
    for i in skp:
        new_duty = duty.loc[(duty['skp'] == i) & (duty['year_number'] == years[-1])]
        old_duty = duty.loc[(duty['skp'] == i) & (duty['year_number'] == years[-2])]
        old_import = imp.loc[(imp['skp'] == i) & (imp['year_number'] == years[-2])]
        new_duty = new_duty['value'].values
        old_duty = old_duty['value'].values
        old_import = old_import['value'].values
        new_value = (1 + alpha + elasticity[j] * (new_duty[0] - old_duty[0]))*old_import[0]
        imp.loc[(len(imp.index))] = [i,new_value,years[-1]]
        j += 1
    return imp

def first_modul_main(countries:list,skp:list,products:list,duties:list,user_year:int,alpha:float): #we need alpha and end year of prediction
    data = data_reading(countries,skp)
    years = year(data)
    duty = creating_duties(years,data,skp)
    imp = creating_import(years,data,skp)
    elasticity = elasticity_calculating(duty,imp,skp)
    starting_point = years[-1]
    for i in range(starting_point,user_year):
        years = np.append(years,i+1)
        data = adding_new_duties_to_df(data,products,duties,years)
        duty = creating_duties(years,data,skp)
        imp = adding_new_import(years,skp,elasticity,alpha,duty,imp)
        elasticity = elasticity_calculating(duty,imp,skp)
    return imp

#SECOND MODUL

def dollars_to_million_sums(imp:DataFrame,exchange_rate:float):
    imp.loc[:,'value'] *= exchange_rate
    imp.loc[:,'value'] /= 1000
    return imp

def matrix_reading():
    pass

def all_import_export_reading():
    pass

def all_used_resources_final_demand_reading():
    pass

if __name__ == '__main__':
    country_id = ['Армения','Беларусь','Казахстан','Кыргызстан','Российская Федерация']
    skp = ['C13','C14','C15','C21','C29','C30']
    duties = [5,12,25,7,10,15]
    products = ['МЕХ ИСКУССТВЕННЫЙ И ИЗДЕЛИЯ ИЗ НЕГО',
    'ПРЕДМЕТЫ ОДЕЖДЫ И ПРИНАДЛЕЖНОСТИ К ОДЕЖДЕ, ИЗ НАТУРАЛЬНОЙ КОЖИ ИЛИ КОМПОЗИЦИОННОЙ КОЖИ:ПРЕДМЕТЫ ОДЕЖДЫ:ИЗ НАТУРАЛЬНОЙ КОЖИ',
    'ДУБЛ.КОЖА ИЛИ КОЖЕВЕН.КРАСТ ИЗ ШКУР К.Р.С.(ВКЛ. БУЙВОЛ),ЖИВОТ.СЕМ-ВА ЛОШАДИНЫХ,...:ВО ВЛАЖНОМ СОСТ.(ВКЛ.ХРОМИРОВАНН.ПОЛУФАБРИКАТ):НЕШЛИФОВ.ЛИЦЕВЫЕ НЕДВОЕНЫЕ;ЛИЦЕВЫЕ ДВОЕНЫЕ:ИЗ ЦЕЛЫХ ШКУР К.Р.С.(ВКЛ.БУЙВОЛ),ПЛОЩАДЬ ПОВЕРХН.КОТ.< 2,6 М2 (28 КВАДРАТ.ФУТОВ)',
    'КИСЛОТЫ КАРБОНОВЫЕ, СОДЕРЖАЩИЕ ФЕНОЛЬНУЮ ГРУППУ, НО НЕ СОДЕРЖАЩИЕ ДРУГУЮ КИСЛОРОДСОДЕРЖАЩУЮ ФУНКЦИОНАЛЬНУЮ ГРУППУ, ИХ АНГИДРИДЫ, ГАЛОГЕНАНГИДРИДЫ, ПЕРОКСИДЫ, ПЕРОКСИКИСЛОТЫ И ИХ ПРОИЗВОДНЫЕ: САЛИЦИЛОВАЯ КИСЛОТА И ЕЕ СОЛИ',
    'ПРОЧИЕ ИЗДЕЛИЯ ИЗ СВИНЦА:ПРОЧИЕ',
    'ЖЕЛЕЗНОДОРОЖНЫЕ ЛОКОМОТИВЫ, С ПИТАНИЕМ ОТ ВНЕШНЕГО ИСТОЧНИКА ЭЛЕКТРОЭНЕРГИИ, ИЛИ АККУМУЛЯТОРНЫЕ: С ПИТАНИЕМ ОТ ЭЛЕКТРИЧЕСКИХ АККУМУЛЯТОРОВ']
    res = first_modul_main(country_id,skp,products,duties,2035,0.05)
    print(res)