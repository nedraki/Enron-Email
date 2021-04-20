import pandas as pd
import numpy as np
import networkx as nx  #Network analytics
import streamlit as st

#Plots:
import plotly.graph_objects as go
import plotly.express as px
from plots import read_csv


def show_network():

	### File to analyse:

	file_path = 'data/Network_analytics.csv'
	df = pd.read_csv(file_path)

	##########Selection of year of interest: TO BE DEFINED

	df_group = df   #### Passing df to study

#######################################
	## Creating a Graph

	g=nx.Graph()

	### Building nodes and edges:

	for idx, feature in df_group.iterrows():
	    
	    g.add_edge(feature[1],feature[2],weight=feature[3]) #Representing the weight of connection between two people


	#### Create nodes to plot:

	components= nx.connected_components(g)  ### A generator of sets of nodes, one for each component of G
	# components=max(nx.connected_components(g), key=len) ### Getting the the largest connected component

	s = [g.subgraph(c) for c in components]    #sets of nodes

	# # Get positions for the nodes in G
	pos_ = nx.spring_layout(g)
	      
	G = s

	node_x = []
	node_y = []

	

	###################
	text ='1 2 3 TESTING'
	# Custom function to create an edge between node x and node y, with a given text and width
	def make_edge(x, y, text, width):
	    return  go.Scatter(x         = x,
	                       y         = y,
	                       line      = dict(width = width,
	                                   color = '#488'),
	                       hoverinfo = 'text',
	                       text      = ([text]),
	                       mode      = 'lines')
	###############################

	for count, node in enumerate(G[0].nodes()):
	    x, y = pos_[node]
	    node_x.append(x)
	    node_y.append(y)


	node_trace = go.Scatter(
	    x=node_x, y=node_y,
	    mode='markers',
	    hoverinfo='text',
	    marker=dict(
	        showscale=True,
	        # colorscale options
	        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
	        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
	        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
	        colorscale='YlGnBu',
	        reversescale=True,
	        color=[],
	        size=10,
	        colorbar=dict(
	            thickness=15,
	            title='Node Connections',
	            xanchor='left',
	            titleside='right'
	        ),
	        line_width=2))

	### Create edges to plot:

	edge_x = []
	edge_y = []
	edge_trace = [] #For each edge, make an edge_trace, append to list

	poi = 0 

	for edge in G[poi].edges():
	    
	    weight_edge = G[poi].edges()[edge]['weight']
	    
	#     if G[poi].edges()[edge]['weight'] > 1:

	    char_1 = edge[0]
	    char_2 = edge[1]
	    x0, y0 = pos_[char_1]
	    x1, y1 = pos_[char_2]
	    
	##################
	    trace  = make_edge([x0, x1, None], [y0, y1, None], text, 
	                               width = 0.2*weight_edge**1.1)
	    edge_trace.append(trace)
	##################

	    edge_x.append(x0)
	    edge_x.append(x1)
	    edge_x.append(None)
	    edge_y.append(y0)
	    edge_y.append(y1)
	    edge_y.append(None)
	    
	##########################################################################""

	node_adjacencies = []
	node_text = []
	for node, adjacencies in enumerate(G[poi].adjacency()):
	    node_adjacencies.append(len(adjacencies[1]))
	    node_text.append(' '+str(adjacencies[0]))


	node_trace.marker.color = node_adjacencies    #### Color or size???? trace.marker.color or .size
	node_trace.text = node_text



	#################
	# Customize layout
	layout = go.Layout(
	#     paper_bgcolor='rgba(0,0,0,0)', # transparent background
	#     plot_bgcolor='rgba(0,0,0,0)', # transparent 2nd background
	    xaxis =  {'showgrid': False, 'zeroline': False}, # no gridlines
	    yaxis = {'showgrid': False, 'zeroline': False}, # no gridlines
	)
	################

	### Create Network Graph:

	# Create figure
	fig = go.Figure(layout = layout)
	# Add all edge traces
	for trace in edge_trace:
	    fig.add_trace(trace)
	# Add node trace
	fig.add_trace(node_trace)
	# Remove legend
	fig.update_layout(showlegend = False)
	# Remove tick labels
	fig.update_xaxes(showticklabels = False)
	fig.update_yaxes(showticklabels = False)
	# Show figure
	# fig.show()
	st.write(fig)


	### The bubbles have the size according with the number of total email connections

	return fig