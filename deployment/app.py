import pandas as pd
import numpy as np
import streamlit as st

#Plots:
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plots import read_csv, time_workload, bar_plot_interactive, plot_hiring
from plots_emails import bar_plots_emails, bar_plots_emails_historical
from network_visuals import show_network
from sentiments import i_got_a_feeling, give_emoji_sentiment, give_emoji_subjectivity
from Network_analytics import graph_nx_class, make_graph_nx, make_graph_nx_weight, make_subgraph_nx
from sentiment_scores import WC
from PIL import Image, ImageOps

### Sidebar selection options:

st.sidebar.title("Visualization Selector")
st.sidebar.markdown("Select the Charts/Plots accordingly:")


select = st.sidebar.selectbox('Email traffic', ['Historical','2000','2001', '2002'], key='1')
select_network = st.sidebar.selectbox('Networks', ['Full Network','Subset Network'], key='1')
select_unit_feel = st.sidebar.selectbox('Feelings', ['HR','Management', 'Federal legislation'], key='1')
select_unit = st.sidebar.selectbox('Business Unit', ['HR','Management', 'Online Trading'], key='1')




#### Graphs:


st.header('Testing')
st.write('Hello Team')

file_path = 'data/enron_subset_10kemails.csv'
dataset = read_csv(file_path)

dataset_networks = pd.read_csv('data/Network_analytics_processed.csv')


###########################################
	# Plotting relevant data:
###########################################

#Email's traffic visual representation

if select == 'Historical':
	bar_plots_emails_historical(dataset)
elif select == '2000':
	bar_plots_emails(dataset, 2000)
	st.write(plot_hiring(2000))
elif select == '2001':
	bar_plots_emails(dataset, 2001)
	st.write(plot_hiring(2001))
elif select == '2002':
	bar_plots_emails(dataset, 2002)
	st.write(plot_hiring(2002))


# Business unit visual representation:

if select_unit == 'HR':
	fig = st.write(WC('hr'))
elif select_unit == 'Management':
	fig = st.write(WC('management'))
elif select_unit == 'Online Trading':
	fig = st.write(WC('online trading'))

#### Network analytics visual representation:

if select_network == 'Full Network':

	G, pos_ = graph_nx_class(dataset_networks)
	st.subheader('Network of employees in Enron')
	st.write(make_graph_nx(G,pos_,'color'))

	st.subheader(" The 'Bubbles' are indicators of employees with more connections")
	st.write(make_graph_nx(G,pos_, 'size'))

elif select_network == 'Subset Network':
	st.sidebar.text('Working on code')

	G, pos_ = graph_nx_class(dataset_networks)
	poi = 0 #### IDEALMENTE EL USUARIO ELIGE POI
	st.subheader('Subgraph with highest number of connections:')
	st.write(make_subgraph_nx(G, poi))



#### Sentiment analysis:

if select_unit_feel == 'HR':
	
	st.subheader('HR Department')
	
	folder = 'hr'
	sent, subjec = i_got_a_feeling(folder)

	image = Image.open(f'data/{folder}/topemotion_{folder}.jpg')
	st.image(image, width=720)

	image = Image.open(f'data/{folder}/houremotion_{folder}.jpg')
	st.image(image, width=720)

	image = Image.open(f'data/{folder}/workemotion_{folder}.jpg')
	st.image(image, width=720)

elif select_unit_feel == 'Management':
	st.subheader('Management')

	folder = 'management'
	sent, subjec = i_got_a_feeling(folder)

	image = Image.open(f'data/{folder}/topemotion_{folder}.jpg')
	st.image(image, width=720)

	image = Image.open(f'data/{folder}/houremotion_{folder}.jpg')
	st.image(image, width=720)

	image = Image.open(f'data/{folder}/workemotion_{folder}.jpg')
	st.image(image, width=720)


elif select_unit_feel == 'Federal legislation':
	st.subheader('Federal legislation')

	folder = 'federal legislation'
	sent, subjec = i_got_a_feeling(folder)

	image = Image.open(f'data/{folder}/topemotion_{folder}.jpg')
	st.image(image, width=720)

	image = Image.open(f'data/{folder}/houremotion_{folder}.jpg')
	st.image(image, width=720)

	image = Image.open(f'data/{folder}/workemotion_{folder}.jpg')
	st.image(image, width=720)

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




