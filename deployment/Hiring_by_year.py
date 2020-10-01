#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os


def plot_hr_metrics():

    filepath = os.path.abspath('../data/Enron_Kaggle_dataset/Enron_by_year') # 3K emails
    df = pd.read_csv(filepath)
    #converting the Date column into datetime type
    df=dataset
    df["Date"] = pd.to_datetime(df["Date"])
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



