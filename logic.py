
from new_app.libs.psql import db_clint
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression



def elast_modul(countries:list,skp:list):
    database = db_clint.read_sql()
    country_filter = database['country_name'].isin(countries)
    df_with_filter = database[country_filter]
    skp_filter = df_with_filter['skp'].isin(skp)
    df_with_filter = df_with_filter[skp_filter]
    years = df_with_filter['year_number'].unique()
    columns = ['skp','value','year']
    duty = pd.DataFrame(columns=columns)
    imp = pd.DataFrame(columns=columns)
    for i in years:
        for j in skp:
            frame = df_with_filter[(df_with_filter['year_number'] == i) & (df_with_filter['skp'] == j)]
            duty.loc[len(duty.index)] = [frame['skp'].unique(),frame['duty'].mean(),frame['year_number'].unique()]
            imp.loc[len(imp.index)] = [frame['skp'].unique(),frame['price'].sum(),frame['year_number'].unique()]
    coef = np.empty((len(skp),2))
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
    elast = np.empty(len(skp))
    row = 0
    for i in skp:
        duty_frame = duty[duty['skp'] == i]
        imp_frame = imp[imp['skp'] == i]
        if not (np.isnan(coef[row,1])):
            elast[row] = coef[row,1]*(duty_frame['value'].mean()/imp_frame['value'].mean())
        else:
            elast[row] = 'NaN' # or NULL
        row += 1
    



# <<<<<<< HEAD
# if __name__== "__main__":
#     country_id = [377, 379, 380]
#     country_id = [9753,9754]
#     a = test(country_id, country_id)
#     # print(a)
# =======
# if __name__ == '__main__':
#     country_id = ['Армения','Беларусь','Казахстан','Кыргызстан','Российская Федерация']
#     skp = ['C13','C14','C15','C21','C29','C30']
#     a = elast_modul(country_id,skp)
#     #print(a)
# >>>>>>> 023c669e16f5aa4fec54cd77531a94feef70b993
