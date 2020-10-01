import pandas as pd
import numpy as np
import random
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


### Selector:

mark_title = st.empty()
my_title = mark_title.title('Enron detective')
mark_sub = st.empty()
my_subheader = mark_sub.subheader("The dashboard will help you find insights for your investigation")


feature_selector = st.multiselect("What insights would you like to find: ", ['Email traffic',
								'Network analytics',
								'Sentiments',
								'Business unit'] )

### Sidebar selection options:

sidebar_title = st.sidebar.title("Visualization Selector")
my_sidebar = st.sidebar.markdown("Select the Charts/Plots accordingly:")

placeholder = st.empty()
	
## Datasets:

file_path = 'data/enron_subset_10kemails.csv'
dataset = read_csv(file_path)

dataset_networks = pd.read_csv('data/Network_analytics_processed.csv')


###########################################
	# Plotting relevant data:
###########################################

#Email's traffic visual representation


if 'Email traffic' in feature_selector:

	placeholder.empty()
	mark_title.empty()
	mark_sub.empty()

	select = st.sidebar.selectbox('Emails', ['Historical','2000','2001', '2002'], key='1')

	if select == 'Historical':
		st.subheader("Emails sent during last years of Enron's operations")
		st.markdown("---")
		bar_plots_emails_historical(dataset)
	elif select == '2000':

		st.subheader("Email's traffic in year 2000")
		st.markdown("---")
		bar_plots_emails(dataset, 2000)
		st.info("The quantity of emails sent by month increased progressively during the year 2000.")
		st.info("Most of the work is done in office hours.")
		st.markdown("---")

		st.subheader("New sended emails")
		st.markdown("---")
		st.write(plot_hiring(2000))
		st.info("People was progressively joining to the workforce")
		st.info("2000 was a year of continuos hiring for the company")
		st.markdown("---")

	elif select == '2001':
		st.subheader("Email's traffic in year 2001")
		st.markdown("---")
		bar_plots_emails(dataset, 2001)
		st.info("Enron employees are taking summer vacations in 2001")
		st.info("Work overload: journeys are extended until night")
		st.markdown("---")

		st.subheader("New sended emails")
		st.markdown("---")
		st.write(plot_hiring(2001))
		st.markdown("---")

	elif select == '2002':
		st.subheader("Email's traffic in year 2002")
		st.markdown("---")
		bar_plots_emails(dataset, 2002)
		st.info("After the scandal, operations show a drastic decline")
		st.markdown("---")

		st.subheader("New sended emails")
		st.markdown("---")
		st.write(plot_hiring(2002))
		st.markdown("---")

# Business unit visual representation:

if 'Business unit' in feature_selector:

	placeholder.empty()
	mark_title.empty()
	mark_sub.empty()
	
	select_unit = st.sidebar.selectbox('Business unit', ['HR','Management','Federal legislation','Online Trading','KPMG'], key='2')

	if select_unit == 'HR':
		st.subheader("Human resources talked about:")
		st.markdown("---")
		fig = st.write(WC('hr'))
		st.markdown("---")

	elif select_unit == 'Management':
		st.subheader("Managers were focused on:")
		st.markdown("---")
		fig = st.write(WC('management'))
		st.markdown("---")

	elif select_unit == 'Online Trading':

		st.subheader("Are the traders talking about wall street? ")
		st.markdown("---")

		fig = st.write(WC('online trading'))
		st.markdown("---")		

	elif select_unit == 'Federal legislation':
		st.subheader("What about institutions? ")
		st.markdown("---")
		fig = st.write(WC('federal legislation'))
	elif select_unit == 'KPMG':		
		st.subheader("Auditors want to talk...")
		st.markdown("---")

		fig = st.write(WC('kpmg'))
		st.markdown("---")


#### Network analytics visual representation:

if 'Network analytics' in feature_selector:

	placeholder.empty()
	mark_title.empty()
	mark_sub.empty()
	
	select_network = st.sidebar.selectbox('Networks', ['Full Network','Subset Network'], key='1')

	if select_network == 'Full Network':

		G, pos_ = graph_nx_class(dataset_networks)
		st.subheader('Connections among employees')
		st.markdown("---")
		st.write(make_graph_nx(G,pos_,'color'))
		st.info("You can zoom in to reveal the networks")
		st.markdown("---") 

		st.subheader(''' The "Bubbles" are indicators for higher number of connections''')
		st.write(make_graph_nx(G,pos_, 'size'))

	elif select_network == 'Subset Network':
		st.sidebar.text('Working on code')

		G, pos_ = graph_nx_class(dataset_networks)
		poi = 0 #### IDEALMENTE EL USUARIO ELIGE POI
		st.subheader('Network subgraph')
		st.write(make_subgraph_nx(G, poi))
		order = st.button('See other subgraph')

		if order:
			poi = random.randint(1,61)
			st.write(make_subgraph_nx(G, poi))



#### Sentiment analysis:

if 'Sentiments' in feature_selector:

	placeholder.empty()
	mark_title.empty()
	mark_sub.empty()
	

	select_unit_feel = st.sidebar.selectbox('Sentiments', ['HR','Management', 'Federal legislation', 'KPMG'], key='4')

	if select_unit_feel == 'HR':

		st.subheader('HR Department')
		st.markdown("---")
		folder = 'hr'
		sent, subjec = i_got_a_feeling(folder)

		image = Image.open(f'data/{folder}/topemotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")
		image = Image.open(f'data/{folder}/houremotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")
		image = Image.open(f'data/{folder}/workemotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")

	elif select_unit_feel == 'Management':

		st.subheader('Management')
		st.markdown("---")

		folder = 'management'
		sent, subjec = i_got_a_feeling(folder)

		st.markdown("---")
		image = Image.open(f'data/{folder}/topemotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")
		image = Image.open(f'data/{folder}/houremotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")
		image = Image.open(f'data/{folder}/workemotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")

	elif select_unit_feel == 'Federal legislation':

		st.subheader('Federal legislation')
		st.markdown("---")
		folder = 'federal'
		# sent, subjec = i_got_a_feeling(folder)

		image = Image.open(f'data/{folder}/topemotion_{folder}.jpg')

		st.image(image, width=720)
		st.markdown("---")
		image = Image.open(f'data/{folder}/houremotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")
		image = Image.open(f'data/{folder}/workemotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")

	elif select_unit_feel == 'KPMG':

		st.subheader('KPMG')
		st.markdown("---")
		folder = 'kpmg'
		# sent, subjec = i_got_a_feeling(folder)

		image = Image.open(f'data/{folder}/topemotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")
		image = Image.open(f'data/{folder}/houremotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")
		image = Image.open(f'data/{folder}/workemotion_{folder}.jpg')
		st.image(image, width=720)
		st.markdown("---")


#### Necesary further: ###################

#### Building selection buttons


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




