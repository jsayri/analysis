# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from covid19_analysis import __version__

__author__ = "J SAYRITUPAC"
__copyright__ = "J SAYRITUPAC"
__license__ = "mit"

def recreate_df(raw_df):
    '''Create a dataframe based on the DF provide by the JHU repository'''
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


def safe_div(x,y):
    ''' Calculate a division between two vector on which the divisor have a zero value. The final result will have zero as well'''
    isZero = (y == 0)
    y2 = np.array(y)
    y2[isZero] = 1
    res = x / y2
    res[isZero] = 0
    return res