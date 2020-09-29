import pandas as pd
import numpy as np
import streamlit as st

#Plots:
import plotly.graph_objects as go
import plotly.express as px
from plots import read_csv, time_workload, bar_plot_interactive



#### Functions for interactive plots:

#########################################################


#### Graphs:


st.header('Testing')
st.write('Hello Team')

file_path = 'data/enron_subset_10kemails.csv'
dataset = read_csv(file_path)

#### Building selection buttons

if st.button('Display data'):
	st.write(dataset.head())
	st.button('Hide data')
elif st.button('Hide data'):
	st.write('Data is hidden')


###########################################
	# Plotting relevant data:
###########################################


#### Yearly plot: 

data = time_workload(dataset,'email-body', 'year', None, normalized=True)

### Updating figure to timeframe of interest :

data = data[data.index > 1998]
data = data[data.index < 2003]
fig = bar_plot_interactive(data,'freq', 'Emails sent by year', '%')
st.write(fig)

#### Monthly: 

year_of_interest = 2001
data = time_workload(dataset, 'email-body', 'month', year_of_interest)
fig = bar_plot_interactive(data, 'freq', 'Emails  sent by month', '%')

### Layout for figure:

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Emails",
    legend_title="Legend Title")

st.write(fig)


#### Hourly:

year_of_interest = 2000
data = time_workload(dataset, 'email-body', 'hour', year_of_interest)
fig = bar_plot_interactive(data, 'freq', 'Emails sent by hour', '%')

### Layout for figure:

fig.update_layout(
    xaxis_title="Hour of the day",
    yaxis_title="Emails",
    legend_title="Legend Title")

st.write(fig)


#########################



#### Building a checkbox

bar_plot = st.checkbox('Bar plot')
line_chart = st.checkbox('Line Chart')

if bar_plot:
	st.write('Great!')
	st.write(fig)
	#st.plotly_chart(fig)
elif line_chart:
	st.write('Wise election')
	#st.line_chart(data.Fare)


end = st.button('Did you finish the tutorial?')
if end:
	st.success('Congratulations, you have completed the tutorial')




