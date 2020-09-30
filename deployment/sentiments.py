import pandas as pd
import numpy as np
import networkx as nx  #Network analytics
import streamlit as st


import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer, PorterStemmer
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
import nltk
nltk.download('stopwords')


#Plots:
import plotly.graph_objects as go
import plotly.express as px
from plots import read_csv
import emoji

	
	

def i_got_a_feeling(unit_of_interest):

	file_path = 'data/enron_subset_10kemails.csv'
	df = pd.read_csv(file_path)
	df_email = df

	def preprocess_folder(data):   
	    folders = []
	    for item in data:
	        if item is None or item is '':
	            folders.append(np.nan)
	        else:
	            item = str(item).split('\\')[-1]
	            item = item.lower()
	            folders.append(item)
	    print("Folder cleaned!")
	    return folders


	df_email["X-Folder"] = preprocess_folder(df_email["X-Folder"])

	# Folders we can filter out
	unwanted_folders = ["all documents", "discussion threads", "sent","inbox",
	                   "sent items", "'sent mail", "untitled", "notes inbox", "junk file", "calendar"]

	# A new dataframe without non-topical folders
	df_folder = df_email.loc[~df_email['X-Folder'].isin(unwanted_folders)]

	print(df_folder.iloc[:15]["X-Folder"].value_counts())


	#### Department of interest

	hr = df_folder.loc[df_folder['X-Folder'] == unit_of_interest]

	## Change the reviews type to string
	hr['reviews.text'] = hr['email-body'].astype(str)

	## Lowercase all reviews
	hr['reviews.text'] = hr['reviews.text'].apply(lambda x: " ".join(x.lower() for x in x.split()))

	stop = stopwords.words('english')

	hr['reviews.text'] = hr['reviews.text'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

	pst = PorterStemmer()

	hr['reviews.text'] = hr['reviews.text'].apply(lambda x: " ".join([pst.stem(word) for word in x.split()]))

	## Define a function which can be applied to calculate the score for the whole dataset

	def senti(x):
	    return TextBlob(x).sentiment  

	hr['senti_score'] = hr['reviews.text'].apply(senti)

	hr.senti_score.head()

	## Iterate on items of senti_score to save values on list
	polarity = []
	subjective = []
	for idx, score in hr.senti_score.iteritems():
	    polarity.append(score[0])
	    subjective.append(score[1])
	    
	### What is the overall feeling in the department ?

	overall_polarity = np.mean(polarity)
	print(f'Overall Polarity:',overall_polarity)
	overall_subjectivity = np.mean(subjective)
	print(f'Overall Subjectivity:',overall_subjectivity)

	# Polarity is float which lies in the range of [-1,1] 
	# 1 means positive statement
	# -1 means a negative statement

	# Subjectivity is a float within the range [0.0, 1.0]
	# 0.0 is very objective 
	# 1.0 is very subjective,

	###Type of scores must be checked; it should be numerical

	### Sentiments as emojies:

	### Visual results: 

	give_emoji_sentiment(overall_polarity)
	give_emoji_subjectivity(overall_subjectivity)


	return overall_polarity, overall_subjectivity


def give_emoji_sentiment(score):
	    
	    if score == 0:
	        st.write(f'Happiness: {round(score*100)}% ')
	        st.write(emoji.emojize("Too many poker faces :expressionless:", use_aliases=True))
	    elif (score >0 and score <0.5):
	        st.write(f'Happiness: {round(score*100)}% ')
	        st.write(emoji.emojize("People is slightly happy :blush: ", use_aliases=True))
	    elif score > 0.5:
	        st.write(f'Happiness: {round(score*100)}% ')
	        st.write(emoji.emojize("Happy people :smile:", use_aliases=True))
	    else:
	        st.write(f'Happiness: {round(score*100)}% ')
	        st.write(emoji.emojize("Angry birds :angry:", use_aliases=True))

	          
	        
def give_emoji_subjectivity(score):
    
    if score == 0: #Very objective
        st.write(emoji.emojize("A :100:% objective department :speech_balloon: :memo:", use_aliases=True))
    elif score == 1: #Very subjective
        st.write(emoji.emojize("A very subjective department :thought_balloon:", use_aliases=True))
    else:
        st.write(emoji.emojize(f"{100 - round(score*100)}% Objective :thought_balloon: ", use_aliases=True))
