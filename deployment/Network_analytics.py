import pandas as pd
import numpy as np
import os
#Plots:
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx

def graph_nx_class(dataset):
    
    ## Creating a Graph class

    G = nx.Graph()

    ### Assigning nodes and edges:

    for idx, feature in dataset.iterrows():

        G.add_edge(feature[1],feature[2],weight=feature[3]) #Representing the weight of connection between two people

    ### Layout for graphs:

    pos_ = nx.spring_layout(G)    ### A layout for displaying better the subgraphs
    
    return G, pos_


def make_graph_nx(G,pos_,mode):
    
    #### Create nodes to plot:

    node_x = []
    node_y = []

    for count, node in enumerate(G.nodes()):
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
            colorscale='Portland',
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
    
#####################################################

    ### Create edges to plot:

    edge_x = []
    edge_y = []

    for edge in G.edges():

        weight_edges = G.edges()[edge]['weight']

        char_1 = edge[0]
        char_2 = edge[1]
        x0, y0 = pos_[char_1]
        x1, y1 = pos_[char_2]

        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

        edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width= 0.8*weight_edges**2, color='#888'),   ###Define the line connecting nodes
        hoverinfo='none',
        mode='lines')
        
################################################
        
    node_adjacencies = []
    node_text = []

    for node, adjacencies in enumerate(G.adjacency()):

        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('#Employee: '+str(adjacencies[0]))

#     node_trace.marker.size = node_adjacencies    
#     node_trace.text = node_text
    
    if mode == 'color':
        node_trace.marker.color = node_adjacencies    
        node_trace.text = node_text
    elif mode == 'size':
        node_trace.marker.size = node_adjacencies    
        node_trace.text = node_text
        
    
###########################################################""

    ### Plot results:

    fig = go.Figure(data=[edge_trace, node_trace],
         layout=go.Layout(
            title='<br>Testing Network graph made with Python',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="1,2,3 Testing",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002 ) ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            )

    return fig


def make_subgraph_nx(G, poi):


    # A generator of sets of nodes, one for each component of G
    # Generate a sorted list of connected components, largest first.

    pos_ = nx.spring_layout(G)
    components= sorted(nx.connected_components(G), key=len, reverse=True)


#     #Getting sets of nodes:

    s = [G.subgraph(c) for c in components]
    print('Available nx subsets :',len(s))
    G = s

    node_x = []
    node_y = []

    text =' '

    ###################


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

    for count, node in enumerate(G[poi].nodes()):
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


    for edge in G[poi].edges():

        weight_edge = G[poi].edges()[edge]['weight']

        char_1 = edge[0]
        char_2 = edge[1]
        x0, y0 = pos_[char_1]
        x1, y1 = pos_[char_2]

    ##################
        trace  = make_edge([x0, x1, None], [y0, y1, None], text, 
                                   width = 0.2*weight_edge**1.5)
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
    
    return fig



def make_graph_nx_weight(G, pos_):


    # A generator of sets of nodes, one for each component of G
    # Generate a sorted list of connected components, largest first.

    components= sorted(nx.connected_components(G), key=len, reverse=True)


    node_x = []
    node_y = []

    text =' '

    ###################


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

    for count, node in enumerate(G.nodes()):
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
            colorscale='Viridis',
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


    for edge in G.edges():

        weight_edge = G.edges()[edge]['weight']

        char_1 = edge[0]
        char_2 = edge[1]
        x0, y0 = pos_[char_1]
        x1, y1 = pos_[char_2]

    ##################
        trace  = make_edge([x0, x1, None], [y0, y1, None], text, 
                                   width = 0.1*weight_edge**2)
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
    
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(' '+str(adjacencies[0]))


    node_trace.marker.color = node_adjacencies   
    node_trace.text = node_text

    #################
    # Customize layout
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', # transparent background
    #     plot_bgcolor='rgba(0,0,0,0)', # transparent 2nd background
        xaxis =  {'showgrid': False, 'zeroline': False}, # no gridlines
        yaxis = {'showgrid': False, 'zeroline': False}, # no gridlines
    )
    ################

    ### Create Network Graph:

    # Create figure
    fig = go.Figure()
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
    
    return fig

