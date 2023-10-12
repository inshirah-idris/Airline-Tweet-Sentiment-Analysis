# -*- coding: utf-8 -*-
"""Airline Tweet Sentiment Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SbRPD6jo7Z4PfXCft6i0nIY0N3xt3neI

# **Airline Tweet Sentiment Analysis**

**Introduction**

The objective of this project is to conduct sentiment analysis on airline customers' feedback on Twitter, employing various machine learning classifiers. We used the Twitter US Airline Sentiment dataset that had already been annotated with sentiment labels, but for the purpose of making the analysis more comprehensive we ignored them.

---

**Project Description**

The project was divided into four main phases:
  *   Preprocessing
  *   Labeling
  *   Feature Extraction
  *   Classification

---

**Source of Data:**

https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment/data

## **Python Libraries**
"""

# Loading Libraries
import numpy as np
import pandas as pd

# Data Processing
import re
import string
import emoji
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Data Labelling
from textblob import TextBlob

# Analysis and Visualisation
from tabulate import tabulate
from wordcloud import WordCloud
import matplotlib
from matplotlib import pyplot as plt

# Feature Extraction
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer

# Clasiffication
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier

"""## **Data Uploading**"""

from google.colab import drive
drive.mount('/content/drive')

df_org = pd.read_csv('File Path/Tweets.csv')

df = df_org[['tweet_id','airline','text']]

"""## **Preprocessing**"""

def pre_process(tweet):
    # Replace @username with empty string
    tweet = re.sub('@[^\s]+','', tweet)
    # Replace www.* or https?://* with empty string
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','', tweet)
    # Replace #word with with empty string
    tweet = re.sub('#([^\s]+)','', tweet)
    # Replace the numbers with empty string
    tweet = re.sub('\d+','', tweet)
    # Replace punctuations Replace
    tweet = re.sub('[^\w\s]','', tweet)
    # Convert the alphabet to lowercase
    tweet = str(tweet).lower()
    return tweet

# Applying processPost function for preprocessing
df['clean_text'] = df['text'].apply(lambda x: pre_process(x))

# Replace emoji with empty string
df['clean_text'] = df['clean_text'].apply(lambda s: emoji.replace_emoji(s, ''))
# Remove the daplicate raw
df = df.drop_duplicates()
# Tokenize the tweet text
df['clean_text'] = df['clean_text'].apply(nltk.word_tokenize)
# Remove the stop words
stopwords_list = stopwords.words('english')
df['clean_text'] = df['clean_text'].apply(lambda x:[item for item in x if item not in stopwords_list])
# lemmatize the tweet text
lemmatizer  = WordNetLemmatizer()
df['clean_text'] = df['clean_text'].apply(lambda x:[lemmatizer .lemmatize(word) for word in x])

"""## **Labilling**"""

# TextBlob Data Lablling
df['Sentiment'] = ''
for i,x in df.text.iteritems():
    label = TextBlob(x)
    df['Sentiment'][i] = label.sentiment.polarity
def polarity_to_label(x):
    if(x >= -1 and x < 0):
        return 'Negative'
    if(x == 0):
        return 'Neutral'
    if(x > 0 and x <= 1):
        return 'Positive'
df.Sentiment = df.Sentiment.apply(polarity_to_label)

"""## **Analysis and Visualisation**"""

# Count total number of tweets
Tweets_Count = len(df)
# Count number of unique users
Unique_Users = len(df['tweet_id'].unique())
dict_Tweets  = {'Name': ['Tweets_Count', 'Unique User_Count'], 'Count': [Tweets_Count, Unique_Users]}
head = ["Name", "Count"]
print(tabulate(dict_Tweets, headers=head, tablefmt="grid"))

# Wordcloud generation for all tweets
all_words = df['clean_text'].to_string(index=False)
word_cloud = WordCloud(width=800, height=500, random_state=21,max_font_size=110,colormap='tab20').generate(all_words)
plt.figure(figsize=(10, 7))
plt.imshow(word_cloud)
plt.axis('off')
plt.show()

# People's feelings towards the airline companies
matplotlib.style.use('tableau-colorblind10')
df['Sentiment'].value_counts().plot.pie(autopct='%1.1f%%', wedgeprops={'linewidth':2.0, 'edgecolor': 'white'}, textprops={'fontsize':10})
plt.title("People's feelings Towards the Airline Companies", fontsize=14)
plt.axis('equal')
plt.show()

df['Sentiment'].value_counts()

# creates a stacked bar plot
matplotlib.style.use('tableau-colorblind10')
crossplt = pd.crosstab(df['airline'], df['Sentiment'])
crossplt.plot(kind="bar", stacked=True)
plt.yticks(fontsize="8")
plt.xticks(rotation=30, horizontalalignment="center", fontsize="8")
plt.title("public Perception Per each Company", fontsize="14")
plt.xlabel("Airline Companies", fontsize="12")
plt.ylabel("Custmer Opinions", fontsize="12")
plt.legend(fontsize="8")

"""## **Features Extraction**"""

# TF-IDF features extraction
tfidf_vectorizer = TfidfVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(df['clean_text'].astype('str'))
unigramdataGet = tfidf.toarray()
vocab = tfidf_vectorizer.get_feature_names_out()
features = pd.DataFrame(np.round(unigramdataGet, 1), columns=vocab)
features[features>0] = 1
pro = preprocessing.LabelEncoder()
encpro = pro.fit_transform(df['Sentiment'])
df['label'] = encpro
y = df['Sentiment']
X = features

"""## **Classification**"""

# Spliting Dataset into 70% Training and 30% Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=333)

# Naive Bayes Algorithm
nb = GaussianNB()
nb = nb.fit(X_train , y_train)
y_pred = nb.predict(X_test)
nbg = nb.score(X_test, y_test)
print('Accuracy= {:.3f}'.format(nb.score(X_test, y_test)))

# LogisticRegression Algorithm
LR = LogisticRegression(penalty = 'l2', C = 1)
LR = LR.fit(X_train , y_train)
y_pred = LR.predict(X_test)
lr = LR.score(X_test, y_test)
print('Accuracy= {:.3f}'.format(LR.score(X_test, y_test)))

# SVM Algorithm
SVCModel = SVC(kernel= 'poly',max_iter=100,C=1.0,gamma='auto') # it can be also linear,poly,sigmoid,precomputed
SVCModel.fit(X_train, y_train)
y_pred = SVCModel.predict(X_test)
svm =SVCModel.score(X_test, y_test)
print('Accuracy= {:.3f}'.format(SVCModel.score(X_test, y_test)))

# Neural Network Algorithm
MLPClassifierModel = MLPClassifier(activation='relu', # can be also identity , logistic , relu
                                   solver='lbfgs',  # can be also sgd , adam
                                   learning_rate='constant', # can be also invscaling , adaptive
                                   early_stopping= False,max_iter=200,
                                   alpha=0.0001 ,hidden_layer_sizes=(100, 3),random_state=99)
MLPClassifierModel.fit(X_train, y_train)
y_pred = MLPClassifierModel.predict(X_test)
nn =MLPClassifierModel.score(X_test, y_test)
print('Accuracy= {:.3f}'.format(MLPClassifierModel.score(X_test, y_test)))

# RandomForest Algorithm
clf=RandomForestClassifier(n_estimators=100)
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
RF =clf.score(X_test, y_test)
print('Accuracy= {:.3f}'.format(clf.score(X_test, y_test)))

matplotlib.style.use('tableau-colorblind10')
data = pd.DataFrame({'Classifiers': ['Naive Bayes', 'Logistic Regression', 'SVM', 'MLP', 'Random Forest'],
        'Accuracy': [nbg, lr, svm, nn, RF]})
ax = data.plot(x ='Classifiers', y='Accuracy', kind='bar', legend=False)
for p in ax.patches:
    ax.annotate(f"{p.get_height() * 100:.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', fontsize=8, color='black', xytext=(0, 7),
                 textcoords='offset points')
plt.yticks(fontsize="8")
plt.xticks(rotation=30, horizontalalignment="center", fontsize="8")
plt.title("Evaluating Classifiers Performance", fontsize="14")
plt.xlabel("Classifiers", fontsize="12")
plt.ylabel("Accuracy", fontsize="12")