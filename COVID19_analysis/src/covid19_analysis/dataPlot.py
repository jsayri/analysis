# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import plotly
import datetime


from covid19_analysis import __version__

__author__ = "J SAYRITUPAC"
__copyright__ = "J SAYRITUPAC"
__license__ = "mit"

# Generate cumulative graph over time for JHU dataframe source
def disp_cum_jhu(ts_case, ts_recov, ts_death, loc_name, mask=0):
    '''Routine to display the normal/log tendency of the cumulated cases for JHU datasource only
        ts_case:    <timeserie> information over time for each case
        ts_recov:   <timeserie> information over time for each recovery
        ts_death:   <timeserie> information over time for each fatality
        loc_name:   <string> name of the location under study
        mask:       <boolean> vector with period to display, default=0 all period

        '''
    # check for time filter
    if mask is 0:
        mask = ts_case.index >= ts_case.index[0]

    # Build plot for basic data display
    fig = plotly.graph_objects.Figure()
    # diagnosed cases
    fig.add_trace(
        plotly.graph_objects.Scatter(
            mode='lines+markers',
            x=ts_case.index[mask], 
            y=ts_case[mask],  
            name = 'All cases',
            marker=dict(color='CornflowerBlue')
    ))
    # recover cases
    fig.add_trace(
        plotly.graph_objects.Scatter(
            mode='lines+markers',
            x=ts_recov.index[mask], 
            y=ts_recov[mask],
            name = 'Recover',
            marker=dict(color='forestgreen')
    ))
    # death cases
    fig.add_trace(
        plotly.graph_objects.Scatter(
            mode='lines+markers',
            x=ts_death.index[mask], 
            y=ts_death[mask],  
            name = 'Fatalities',
            marker=dict(color='black')
    ))

    if ts_case.max() > 100:
        fig.update_layout(yaxis_title = 'Cases [Log]', yaxis_type="log")
    else:
        fig.update_layout(yaxis_title = 'Cases')

    fig.update_layout(
        xaxis_title = 'Time [Days]',
        plot_bgcolor='white',  
        title = 'Current situation in ' + loc_name + datetime.datetime.today().strftime(', %B %d, %Y'),
        title_x = .5
    )

    fig.show()


# Generate a graph in original axis with current active cases
def disp_daily_cases(df_data, loc_name, df_source='JHU'):
    '''Display daily cases evolution for confirmed & fatalities for two different data sources. 
        df_data:    <dataframe> daily information per case
        loc_name:   <string> name of the location under study
        pop_factor: <integer> mutiplicative factor for yaxis chart
        
        '''

    if df_source == 'SPF':
        # time vector
        date_time = df_data.date

        # daily cases
        data_tmp = np.array(df_data.cas_confirmes, dtype=int)
        data_tmp[data_tmp<0] = 0
        cases_d = data_tmp[1:]-data_tmp[:data_tmp.size-1]
        cases_d = np.insert(cases_d, 0, data_tmp[0])

        # daily fatalities
        data_tmp = np.array(df_data.deces, dtype=int)
        data_tmp[data_tmp<0] = 0
        death_d = data_tmp[1:]-data_tmp[:data_tmp.size-1]
        death_d = np.insert(death_d, 0, data_tmp[0])

    elif df_source == 'JHU':
        print('not ready yet')
        return

    # Build plot for daily variation
    fig = plotly.graph_objects.Figure()

    # daily cases
    fig.add_trace(
        plotly.graph_objects.Bar(
            x = date_time,
            y = cases_d,
            marker = dict(color = 'CornflowerBlue', line = dict(color = 'darkblue', width=1.5)),
            name = 'Cases'
    ))

    # daily deaths
    fig.add_trace(plotly.graph_objects.Bar(
        x = date_time,
        y = death_d,
        marker = dict(color = 'dimgray', line = dict(color = 'black', width=1.5)),
        name = 'Fatalities'
    ))

    fig.update_layout(
        plot_bgcolor='white', 
        #barmode = 'stack',
        xaxis_title = 'Time [Days]',
        yaxis_title = 'Cases [Hab]',
        title = 'Daily progression in ' + loc_name + datetime.datetime.today().strftime(', %B %d, %Y'),
        title_x = .5
    )
    fig.update_yaxes(showgrid=True, gridwidth=.3, gridcolor='gainsboro')

    fig.show()


# Generate a graph in original axis with current active cases
def disp_current_cases(df_data, loc_name, pop_factor=1):
    '''Display current cases from cumulative and fatalities 
        df_data:    <dataframe> daily information per case
        loc_name:   <string> name of the location under study
        pop_factor: <integer> mutiplicative factor for yaxis chart
        
        '''
    # Calculate current cases from confimed & fatalities
    fat_c = np.array(df_data.deces, dtype=int)
    fat_c[fat_c<0] = 0
    liv_c = np.array(df_data.cas_confirmes, dtype=int) - fat_c
    
    # Build plot for basic data display
    fig = plotly.graph_objects.Figure()
    # Confirmed cases
    fig.add_trace(
        plotly.graph_objects.Bar(
            x=df_data.date, 
            y=liv_c / pop_factor,  
            name = 'On going cases',
            marker=dict(color='CornflowerBlue')
    ))
    # Fatalities
    fig.add_trace(
        plotly.graph_objects.Bar(
            x=df_data.date, 
            y=fat_c / pop_factor, 
            name = 'Fatalities',
            marker=dict(color='Black')
    ))

    fig.update_yaxes(showgrid=True, gridwidth=.3, gridcolor='gainsboro')
    #title= 'Cases, 1 by ' + str(pop_factor) + ' peoples'

    if pop_factor == 1: 
        fig.update_yaxes(title = 'Number of confirmed cases')
    else:
        fig.update_yaxes(title = 'Number of confirmed cases <br>  <sub>factor of 1 by ' + str(format(pop_factor, ",").replace(",", ".")) +' peoples</sub>')
    
    fig.update_layout(
        barmode = 'stack',
        xaxis_title = 'Time [Days]',
        plot_bgcolor='white',  
        title = 'Current active cases in ' + loc_name + datetime.datetime.today().strftime(', %B %d, %Y'),
        title_x = .5
    )
    fig.show()


# Generate a cumulative chart for SPF datasets
def disp_cumulative(df_data, loc_name, pop_factor=1):
    '''Routine to display the normal/log tendency of the cumulated cases
        df_data:        <dataframe> information over time for each case
        loc_name:     <string> name of the location under study
        pop_factor:     <int> multiplicative factor for number of cases
                        default value 1, for other values is display in the 
                        vertical axis the multiplicative magnitude
        
        '''
    fig = plotly.graph_objects.Figure()
    # add scatter chart for confirmed cases
    fig.add_trace(
        plotly.graph_objects.Scatter(
            mode = 'lines+markers',
            x=df_data.date, 
            y=np.array(df_data.cas_confirmes, dtype=int),  
            name = 'Confirmed cases',
            marker=dict(color='CornflowerBlue'),
    ))
    # add scatter chart for fatalities
    fig.add_trace(
        plotly.graph_objects.Scatter(
            mode='lines+markers',
            x=df_data.date, 
            y=np.array(df_data.deces, dtype=int), 
            name = 'Fatalities',
            marker=dict(color='black')
    ))

    fig.update_layout(yaxis_title = 'Cases [Log]', yaxis_type="log")

    fig.update_layout(
        xaxis_title = 'Time [Days]',
        plot_bgcolor='white',  
        title = 'Current status in ' + loc_name + ' , ' + datetime.datetime.today().strftime('%B %d, %Y'),
        title_x = .5
    )
    fig.update_yaxes(showgrid=True, gridwidth=.3, gridcolor='gainsboro')

    fig.show()