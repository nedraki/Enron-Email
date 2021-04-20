import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os


def read_csv(file_path):

    dataset = pd.read_csv(file_path)

    #Convert date column to datetime 
    dataset["Date"] = pd.to_datetime(dataset["Date"])
    # Adding classification by year to dataframe:
    dataset['year'] = pd.DatetimeIndex(dataset['Date']).year

    return dataset


def time_workload(df, columns, time_frame, year_of_interest, normalized = True):
    
#     time_frame = 'year'
#     dataset = 'df_email'
#     columns = 'email-body'
#     year you want to explore

    dataset = df

    if year_of_interest != None:
        
        ### Data frame with information for year of interest:
        data_year = dataset.loc[dataset['year'] == year_of_interest]
        
        ### Data frame with total for year of interest:
        order = f"data_year.groupby(data_year['Date'].dt.{time_frame}){[[columns]]}.count()"
        data = eval(order)

    else:
        
        data_historical = f"dataset.groupby(dataset['Date'].dt.{time_frame}){[[columns]]}.count()"
        data = eval(data_historical)
    
    if normalized == True:
        
        ### Data normalization (To display percentage)
        total = data.sum()
        data = data/total
        
    data.rename(columns={'email-body':'freq'}, inplace=True)

    return data

def bar_plot_interactive(dataset, y, title, format=None):
    
    fig = px.bar(dataset, y= y, title= title)
    fig.update_xaxes(type='category')
    
    if format == "%":
        fig.update_layout(yaxis_tickformat = '%')

    return fig    
    if format == "%":
        fig.update_layout(yaxis_tickformat = '%')

    return fig

###########################################

def plot_hiring(year_of_interest):

    filepath = 'data/Enron_by_year.csv' # 3K emails
    df = pd.read_csv(filepath)

    #Converting the Date column into datetime type
    
    df["Date"] = pd.to_datetime(df["Date"])

    #Select year: 

    df = df.loc[df['year'] == year_of_interest]

    scatter = px.scatter(df.groupby(["employee"])["Date"].min().sort_values())

    ### Layout for figure:

    scatter.update_layout(
        title="First mail sent",
        xaxis_title="Employee",
        yaxis_title="Date",
        legend_title="Legend",
        xaxis =  {'showgrid': False},
        yaxis = {'showgrid': True})

    return scatter

