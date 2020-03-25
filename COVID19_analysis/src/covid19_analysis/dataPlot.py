# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import plotly
import datetime

# import local functions
import covid19_analysis.dataFun as dataFun
#import covid19_analysis.dataPlot as dataPlot


from covid19_analysis import __version__

__author__ = "J SAYRITUPAC"
__copyright__ = "J SAYRITUPAC"
__license__ = "mit"


# Plot countries growing ratio and doubling time chars
def growing_ratio_countries(df_data, ctry_list, pop_th=100, num_days=37):
    '''Display countries cases over time compare to standards doubling-time ratios
        df_data:    <dataframe> contain all countries daily data
        ctry_list:  <list> string list with countries to display
        pop_th:     <int> population threshold, allows to set chart starting point
        num_days:   <int> set the number of days to display
        
    Graph inspired on the work or Lisa Charlotte ROST, designer & blogger at Datawrapper (March 2020)
    https://lisacharlotterost.de/
    Original graph from Lisa https://www.datawrapper.de/_/w6x6z/ 
    '''

    # build growing rates template
    fig_gr = doublingtime_chart(pop_th, num_days)

    # Extract timeseries & add trace to figure
    for country_name in ctry_list:    
        ts_country = dataFun.get_timeseries_from_JHU(df_data, country_name)

        fig_gr.add_trace(
        plotly.graph_objects.Scatter(
            mode = 'lines',
            #mode = 'lines+markers',
            x = np.array(range(0, ts_country[ts_country > pop_th*.5].size)),
            y = ts_country[ts_country > pop_th*.5],
            name = country_name
        ))
    
    # set graph extra details
    fig_gr.update_layout(
        title = 'Doubling rates per country' + datetime.datetime.today().strftime(', %B %d, %Y'),
        title_x = .5
    )

    fig_gr.show()


# Explore the growing rate over time (call chart growing rate countries)
def doublingtime_chart(pop_th=100, num_days=37):
    '''Build a doubling time chart template
        pop_th:     <int> population threshold, identify min days per contry and set the chart starting point
        num_days:   <int> set the number of days to display
        
    Graph inspired on Lisa Charlotte ROST work https://www.datawrapper.de/_/w6x6z/ 
    '''
    
    # define some working variables
    ndays = np.array(range(0, num_days))
    symbols_list = ['circle', 'square', 'diamond', 'triangle_up', 'cross', 'x', 'asterisk', 'hash']
    gr_array = [1, 2, 3, 5, 7, 30]
    gr_labels = ['daily', 'two days', 'three days', 'five days', 'weekly', 'monthly']
    
    # build a chart template (growing ratios references)
    fig = plotly.graph_objs.Figure()
    for gr_idx, gr_value in enumerate(gr_array):
        # calculate references growing rates
        ncase = dataFun.doubling_time_fun(pop_th, num_days, gr_value)

        # add a growing rate
        fig.add_trace(
            plotly.graph_objs.Scatter(
                #mode = 'lines+markers',
                mode = 'lines',
                name = gr_labels[gr_idx],
                x = ndays,
                y = ncase,
                marker_symbol = 100+2*gr_idx, #select 'open' symbols
                line=dict(color='DarkGray', width = 1.5, dash = 'dashdot'),
                #visible = 'legendonly'
                showlegend=False,
                hoverinfo='skip'
        ))
    
    # anotation style
    annotation_style=dict(size=10, color='DimGray')
    # Text for daily grow
    fig.add_annotation(x = 9, y = 4.7, text = 'Doubles every day', font = annotation_style, arrowcolor='DimGray')
    # Text for 2 days grow
    fig.add_annotation(x = 19, y = 4.85, text = 'Doubles every 2nd day', font = annotation_style, arrowcolor='DimGray')
    # Text for 3 days grow
    fig.add_annotation(x = 29, y = 4.90, text = 'Doubles every 3rd day', font = annotation_style, arrowcolor='DimGray')
    # Text for 5 days grow
    fig.add_annotation(x = 31, y = 3.86, text = 'Doubles every 5th day', font = annotation_style, arrowcolor='DimGray')
    # Text for weekly grow
    fig.add_annotation(x = 33, y = 3.41, text = 'Doubles every week', font = annotation_style, arrowcolor='DimGray')
    # Text for monthly grow
    fig.add_annotation(x = 35, y = 2.40, text = 'Doubles every month', font = annotation_style, arrowcolor='DimGray')

    
    # set chart style and names
    fig.update_yaxes(range=[2, 5.5])
    fig.update_xaxes(range=[0, num_days])
    fig.update_layout(
        yaxis_type="log",
        plot_bgcolor='white', 
        xaxis_title = 'Days',
        yaxis_title = 'Number of cases <br> <sub>Log axe</sub>',
    )
    fig.update_yaxes(showgrid=True, gridwidth=.3, gridcolor='gainsboro')
    #fig.show()
    return fig


# Countries comparison
def disp_countries_comp(df_data, ctry_list, mask=0, plot_type='line'):
    '''Routine to plot countries cases over time so a visual comparison is possible
        df_data:    <dataframe> information from JHU for each case per country over time
        ctry_list:  <list> string list with countries to compare
        mask:       <boolean> vector with period to display, all period by default (0)
        plot_type:  TO BE DONE LATER

    '''
    fig = plotly.graph_objects.Figure()

    for country in ctry_list:
        # get country timeseries
        ctry_ts = dataFun.get_timeseries_from_JHU(df_data, country)

        # check for time filter
        if mask is 0:
            mask = ctry_ts.index >= ctry_ts.index[0]

        if plot_type == 'Bar':
            fig.add_trace(
                plotly.graph_objects.Bar(
                    x = ctry_ts.index[mask],
                    y = ctry_ts[mask], 
                    name = country
                ))

        elif plot_type == 'line':
            fig.add_trace(
                plotly.graph_objects.Scatter(
                    mode = 'lines+markers',
                    x = ctry_ts.index[mask],
                    y = ctry_ts[mask], 
                    name = country
                ))
        
    # set background and axis chart style
    fig.update_layout(
        xaxis_title = 'Time [Days]',
        yaxis_title = 'Cases',
        title = 'COVID-19 cases per country',
        title_x = 0.5,
        plot_bgcolor='white', 
        yaxis_type="log"
    )

    # display horizontal grid lines
    fig.update_yaxes(showgrid=True, gridwidth=.3, gridcolor='gainsboro')

    fig.show()


# Generate recoveries and fatalities rates for JHU dataframe source
def disp_country_rates_jhu(ts_case, ts_recov, ts_death, loc_name, mask=0):
    '''Routine to display the evolution of recovery and fatalies rates compare to all cases reported by JHU datasource
        ts_case:    <timeserie> information over time for each case
        ts_recov:   <timeserie> information over time for each recovery
        ts_death:   <timeserie> information over time for each fatality
        loc_name:   <string> name of the location under study
        mask:       <boolean> vector with period to display, all period by default (0)

        '''
    # Check for time filter
    if mask is 0:
        mask = ts_case.index >= ts_case.index[0]

    # Calculate rates faces to total cases diagnosed
    rate_recov = dataFun.safe_div(ts_recov.values, ts_case.values) *100
    rate_death = dataFun.safe_div(ts_death.values, ts_case.values) *100   

    # display rates
    fig = plotly.subplots.make_subplots(rows=2, cols=1)

    fig.add_bar(
        row=1, col=1,
        x = ts_case.index[mask],
        y = rate_recov[mask],
        name = 'Recoveries',
        marker = dict(color = 'darkseagreen', line=dict(color='forestgreen', width=1.5)),
    )
    fig.update_xaxes(title_text="Time [Days]", row=1, col=1)
    fig.update_yaxes(title_text="Percentage [%]", row=1, col=1, showgrid=True, gridwidth=.3, gridcolor='gainsboro')

    fig.add_bar(
        row=2, col=1,
        x = ts_case.index[mask],
        y = rate_death[mask],
        name = 'Fatalities',
        marker = dict(color = 'DimGray', line=dict(color='Black', width=1.5)),
    )
    fig.update_xaxes(title_text="Time [Days]", row=2, col=1)
    fig.update_yaxes(title_text="Percentage [%]", row=2, col=1, showgrid=True, gridwidth=.3, gridcolor='gainsboro')

    fig.update_layout(
        title_text = 'Recovery & Fatalities rates for ' + loc_name + datetime.datetime.today().strftime(', %B %d, %Y'),
        title_x = .5,
        plot_bgcolor='white')
    
    fig.show()



# Generate cumulative graph over time for JHU dataframe source
def disp_cum_jhu(ts_case, ts_recov, ts_death, loc_name, mask=0):
    '''Routine to display the normal/log tendency of the cumulated cases for JHU datasource only
        ts_case:    <timeserie> information over time for each case
        ts_recov:   <timeserie> information over time for each recovery
        ts_death:   <timeserie> information over time for each fatality
        loc_name:   <string> name of the location under study
        mask:       <boolean> vector with period to display, default=0 all period

        '''
    # Check for time filter
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

    fig.update_yaxes(showgrid=True, gridwidth=.3, gridcolor='gainsboro')
    
    fig.show()


# Generate a graph in original axis with current active cases
def disp_daily_cases(df_data, loc_name, df_source='JHU', mask=0):
    '''Display daily cases evolution for confirmed & fatalities for two different data sources. 
        df_data:    <dataframe> daily information per case
        loc_name:   <string> name of the location under study
        df_source:  <string> select the type of dataframe source
        
        '''
    if df_source == 'SPF':
        # time vector
        date_time = pd.DataFrame(index=df_data.date).index

        # Daily cases
        data_tmp = np.array(df_data.cas_confirmes, dtype=int)
        data_tmp[data_tmp<0] = 0
        cases_d = data_tmp[1:]-data_tmp[:data_tmp.size-1]
        cases_d = np.insert(cases_d, 0, data_tmp[0])

        # daily fatalities
        data_tmp = np.array(df_data.deces, dtype=int)
        data_tmp[data_tmp<0] = 0
        death_d = data_tmp[1:]-data_tmp[:data_tmp.size-1]
        death_d = np.insert(death_d, 0, data_tmp[0])

        # daily recov
        recov_d = 0

    elif df_source == 'JHU':
        # time vector
        date_time = df_data.index

        # Daily cases
        data_tmp = np.array(df_data.cases, dtype=int)
        data_tmp[data_tmp<0] = 0
        cases_d = data_tmp[1:]-data_tmp[:data_tmp.size-1]
        cases_d = np.insert(cases_d, 0, data_tmp[0]).clip(min=0)

        # Daily fatalities
        data_tmp = np.array(df_data.death, dtype=int)
        data_tmp[data_tmp<0] = 0
        death_d = data_tmp[1:]-data_tmp[:data_tmp.size-1]
        death_d = np.insert(death_d, 0, data_tmp[0]).clip(min=0)

        # Daily recovery
        data_tmp = np.array(df_data.recov, dtype=int)
        data_tmp[data_tmp<0] = 0
        recov_d = data_tmp[1:]-data_tmp[:data_tmp.size-1]
        recov_d = np.insert(recov_d, 0, data_tmp[0]).clip(min=0)
        
    else:
        print('Error: Not valid value for df_source')
        return

    # Check for time filter
    if mask is 0:
        mask = date_time >= date_time[0]

    # Build plot for daily variation
    fig = plotly.graph_objects.Figure()

    # daily cases
    fig.add_trace(
        plotly.graph_objects.Bar(
            x = date_time[mask],
            y = cases_d[mask],
            marker = dict(color = 'CornflowerBlue', line = dict(color = 'DarkBlue', width=1.5)),
            name = 'Cases'
    ))

    # daily fatalities
    fig.add_trace(
        plotly.graph_objects.Bar(
            x = date_time[mask],
            y = death_d[mask],
            marker = dict(color = 'DimGray', line = dict(color = 'Black', width=1.5)),
            name = 'Fatalities'
    ))

    if df_source is 'JHU': # exclude SPF
        # daily recoveries
        fig.add_trace(
            plotly.graph_objects.Bar(
                x = date_time[mask],
                y = recov_d[mask],
                marker = dict(color = 'DarkSeaGreen', line = dict(color = 'ForestGreen', width=1.5)),
                name = 'Recoveries'
        ))

    fig.update_layout(
        plot_bgcolor='white', 
        #barmode = 'stack',
        xaxis_title = 'Time [Days]',
        yaxis_title = 'Cases',
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