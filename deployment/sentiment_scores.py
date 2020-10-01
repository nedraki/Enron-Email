import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.corpus import stopwords
import wordcloud

import os
 

def WC(Folder, stpwords = None):

    # taking csv prepared earlier to explore data 

    filepath = "data/Enron_by_year.csv"
    # Read the data into a pandas dataframe called emails

    df = pd.read_csv(filepath)

# Plotting the wordcloud on the basis of sentiment analysis
    
    data = df.loc[df['X-Folder'] == Folder]
    
    stop_words = stopwords.words('english')
    
    list_stpwords = ['Corp','HOU','ECT','Folder','clean','enron', 'com', 're', 'RECIPIENTS', 'CN', 'ENRON', 'OU', 'NA', 'Thank', 'mail', 'know', 'get', 'Thanks', 'one', 'let', 'cc', 'bc', 'subject', 'http', 'www', 'hotmail', 'email', 'would', 'back', 'time', 'bcc','new', 'aol', 'Com', 'Original Message','message']
    
    if stpwords is True:
        
         list_stpwords.append(stpwords) 
        
        
    stop_words.extend(list_stpwords)

    subjects = ' '.join(data['email-body'])

    fig, ax = plt.subplots(figsize=(16, 12))

    wc = wordcloud.WordCloud(width=800,
                             height=600, 
                             max_words=200,
                             stopwords=stop_words).generate(subjects)
    ax.imshow(wc)
    ax.axis("off")
        
    return fig


def plot_emotions(Folder,plot):

    filepath = "data/Enron_by_departments.csv"
    # Read the data into a pandas dataframe called emails
    df = pd.read_csv(filepath)
    
    data = df.loc[df['X-Folder'] == Folder]

    if plot == 'top':
        fig = data.groupby('year').topemotion.value_counts(normalize = True).unstack(0).plot.bar()
    elif plot == 'hour':
        fig = data.groupby('year').time_hour.value_counts(normalize = True).unstack(0).plot.bar()
    elif plot == 'work':
        fig = data.groupby('year').Work.value_counts(normalize = True).unstack(0).plot.bar()
    
    return fig.plot()


    