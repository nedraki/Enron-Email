import pandas as pd
import numpy as np
import streamlit as st

#Plots:
import plotly.graph_objects as go
import plotly.express as px
from plots import read_csv, time_workload, bar_plot_interactive

def bar_plots_emails(dataset,year_of_interest):
#### Yearly plot: 

	data = time_workload(dataset,'email-body', 'year', None, normalized=True)

	### Updating figure to timeframe of interest :

	data = data[data.index > 1998]
	data = data[data.index < 2003]
	fig = bar_plot_interactive(data,'freq', 'Emails sent by year', '%')
	st.write(fig)

	#### Monthly: 

	data = time_workload(dataset, 'email-body', 'month', year_of_interest)
	fig = bar_plot_interactive(data, 'freq', 'Emails  sent by month', '%')

	### Layout for figure:

	fig.update_layout(
	    xaxis_title="Month",
	    yaxis_title="Emails",
	    legend_title="Legend Title")

	st.write(fig)


	#### Hourly:

	data = time_workload(dataset, 'email-body', 'hour', year_of_interest)
	fig = bar_plot_interactive(data, 'freq', 'Emails sent by hour', '%')

	### Layout for figure:

	fig.update_layout(
	    xaxis_title="Hour of the day",
	    yaxis_title="Emails",
	    legend_title="Legend Title")

	st.write(fig)


#########################
