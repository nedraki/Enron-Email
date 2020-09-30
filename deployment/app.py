import pandas as pd
import numpy as np
import streamlit as st

#Plots:
import plotly.graph_objects as go
import plotly.express as px
from plots import read_csv, time_workload, bar_plot_interactive
from plots_emails import bar_plots_emails, bar_plots_emails_historical
from network_visuals import show_network
from sentiments import i_got_a_feeling, give_emoji_sentiment, give_emoji_subjectivity

### Sidebar selection options:

st.sidebar.title("Visualization Selector")
st.sidebar.markdown("Select the Charts/Plots accordingly:")


select = st.sidebar.selectbox('Year of interest', ['Historical','2000','2001', '2002'], key='1')
# select_unit = st.sidebar.selectbox('Business Unit', ['HR','Management', 'Online Trading'], key='1')
select_network = st.sidebar.selectbox('Networks', ['2000','2001', '2002'], key='1')
select_unit_feel = st.sidebar.selectbox('Feelings', ['HR','Management', 'Online Trading'], key='1')


#### Functions for interactive plots:

#########################################################


#### Graphs:


st.header('Testing')
st.write('Hello Team')

file_path = 'data/enron_subset_10kemails.csv'
dataset = read_csv(file_path)



###########################################
	# Plotting relevant data:
###########################################

#Email's traffic visual representation

if select == 'Historical':
	bar_plots_emails_historical(dataset)
elif select == '2000':
	bar_plots_emails(dataset, 2000)
elif select == '2001':
	bar_plots_emails(dataset, 2001)
elif select == '2002':
	bar_plots_emails(dataset, 2002)


# # Business unit visual representation:

# if select_unit == 'HR':
# 	st.sidebar.text("Working on code")
# elif select_unit == 'Management':
# 	st.sidebar.text('Working on code')
# elif select_unit == 'Online Trading':
# 	st.sidebar.text('Working on code')

#### Network analytics visual representation:

if select_network == '2000':
	st.sidebar.text('Working on code')
elif select_network == '2001':
	st.write(show_network())
elif select_network == 'Online Trading':
	st.sidebar.text('Working on code')


#### Sentiment analysis:

if select_unit_feel == 'HR':
	st.subheader('HR Department')
	sent, subjec = i_got_a_feeling('hr')
elif select_unit_feel == 'Management':
	st.subheader('Management')
	sent, subjec = i_got_a_feeling('management')
elif select_unit_feel == 'Online Trading':
	st.subheader('Traders')
	sent, subjec = i_got_a_feeling('online trading')



#### Necesary further: ###################

#### Building selection buttons

st.subheader('Data Frame:')

if st.button('Display data'):
	st.write(dataset.head())
	st.button('Hide data')
elif st.button('Hide data'):
	st.write('Data is hidden')

# #### Building a checkbox

# bar_plot = st.checkbox('Bar plot')
# line_chart = st.checkbox('Line Chart')

# if bar_plot:
# 	st.write('Great!')
# 	st.write(fig)
# 	#st.plotly_chart(fig)
# elif line_chart:
# 	st.write('Wise election')
# 	#st.line_chart(data.Fare)


# end = st.button('Did you finish the tutorial?')
# if end:
# 	st.success('Congratulations, you have completed the tutorial')




