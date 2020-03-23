# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re

from covid19_analysis import __version__

__author__ = "J SAYRITUPAC"
__copyright__ = "J SAYRITUPAC"
__license__ = "mit"

# Provide a timeseries for a define country from JHU dataset
def get_timeseries_from_JHU(df_jhu, country_name, mainland = True):
    '''Provide a timeseries for a define country from JHU dataset. 
        df_jhu:         <dataframe> Dataset read from JHU repository
        country_name:   <string> Name of the country within the JHU country list
        mainland:       <boolean> Allows to choose between have only mainland data or all places data, True by default
        '''
    if country_name is 'all':
        # Calculate the sum of all cases
        temp_array = df_jhu.sum(axis=0, numeric_only=True)
        df_out = df_jhu.head(1).copy()
        for c in temp_array.index:
            if c != 'Lat' and c != 'Long':
                df_out[c] = temp_array[c]

    elif mainland:
        list_province = df_jhu['Province/State'].loc[df_jhu['Country/Region'] == country_name].unique()
        
        # check if exist more than one Province/Region
        if list_province.size > 1:
            print('Warning: %s has many Province/State' %(country_name))
            if any(list_province == country_name):
                print('Warning: Only mainland was taken')
                df_out = df_jhu.loc[(df_jhu['Country/Region'] == country_name) & (df_jhu['Province/State'] == country_name)]
            
            else:
                print('Warning: data for %s is the sum of all Provice/State' %(country_name))
                # calculate aggregate data
                df_tmp = df_jhu.loc[df_jhu['Country/Region'] == country_name]
                if country_name == 'US': # 'US' special case
                    just_states =  [re.search(', ', prov) == None for prov in list_province] 
                    df_tmp = df_tmp.loc[just_states]
                temp_array = df_tmp.sum(axis=0, numeric_only=True)
                df_out = df_tmp.head(1).copy()
                for c in temp_array.index:
                    if c != 'Lat' and c != 'Long':
                        df_out[c] = temp_array[c]
            
        else:
            df_out = df_jhu.loc[df_jhu['Country/Region'] == country_name]
    else:
        # calculate aggregate data
        df_tmp = df_jhu.loc[df_jhu['Country/Region'] == country_name]
        temp_array = df_tmp.sum(axis=0, numeric_only=True)
        df_out = df_tmp.head(1).copy()
        for c in temp_array.index:
            if c != 'Lat' and c != 'Long':
                df_out[c] = temp_array[c]

    # get timeseries
    ts_country = pd.Series(data=df_out.iloc[0][4:].fillna(0).values, index=pd.to_datetime(df_out.columns[4:]), dtype=int)
    return ts_country

# Allow to select one country from the JHU dataset (merger all regions or just mainland)
def select_country(df_all, country_name, just_mainland = True):
    '''Provide a data-frame with the data from the selected country. Note: variable  'just_mainland' equal false,  will sum all Province/States'''
    if just_mainland:
        # check if exist more than one Province/Region
        if df_all['Province/State'].loc[df_all['Country/Region'] == country_name].size > 1:
            print('Warning: %s has more than one Province/State, only mainland was took on the output dataframe' %(country_name))
            df_out = df_all.loc[(df_all['Country/Region'] == country_name) & (df_all['Province/State'] == country_name)]
        else:
            df_out = df_all.loc[df_all['Country/Region'] == country_name]
        return df_out
    else:
        df_tmp = df_all.loc[df_all['Country/Region'] == country_name]
        temp_array = df_tmp.sum(axis=0, numeric_only=True)
        df_out = df_tmp.head(1).copy()
        for c in temp_array.index:
            if c != 'Lat' and c != 'Long':
                df_out[c] = temp_array[c]
        df_out['Province/State'] = country_name
        return df_out

# Define a division for two vectors (array dim 1) when the divisor has zero
def safe_div(x,y):
    ''' Calculate a division between two vector on which the divisor have a zero value. The final result will have zero as well'''
    isZero = (y == 0)
    y2 = np.array(y)
    y2[isZero] = 1
    res = x / y2
    res[isZero] = 0
    return res

# Ancient function. Define a new dataframe from JHU dataframe by reshaping columns by rows and excluding some variables (lat & long)
def recreate_df(raw_df):
    '''OLD FUNCTION: Create a dataframe based on the DF provide by the JHU repository'''
    # identify columns and datetime data
    col_names = raw_df.columns
    date_data = pd.to_datetime(raw_df.columns[4:])
    
    # build columns header as country - province (if not empty)
    region_col = pd.Series(data=raw_df['Province/State'], dtype='str')
    country_col = pd.Series(data=raw_df['Country/Region'], dtype='str')
    col_headers = country_col.str.cat(region_col, sep=(' - '))
    col_headers = col_headers.str.rstrip(' nan').str.rstrip(' -')
    
    # Build dataframe without coordinates and with time as row + countries as columns
    new_df = pd.DataFrame(data=date_data, columns=['Date'])
    for cidx, c in enumerate(col_headers):
        data_tmp = np.array(raw_df.iloc[cidx][4:], dtype=int)
        new_df[c] = data_tmp
    return new_df
