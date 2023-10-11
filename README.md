# Airline-Tweet-Sentiment-Analysis
A comprehensive analysis of public airline sentiment based on the 'Twitter US Airline Sentiment' dataset that is available in Kaggle. The project involves four main stages: tweet preprocessing, sentiment labeling, feature extraction, and sentiment classification.

# Install Necessary Libraries
! pip install emoji

# Dataset:
This project uses the "Twitter US Airline Sentiment" dataset available on Kaggle. The dataset provides a collection of tweets with sentiments about different US airlines. The tweets contain information about the sentiment (positive, neutral, or negative) of six US airline companies.

Link: [Twitter US Airline Sentiment on Kaggle](https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment/data)

# Methodology
The sentiment analysis project was structured according to the following key phases:

## 1. Labeling:
Although the dataset was originally annotated with sentiment labels, we decided to follow our own labeling for a more comprehensive analysis. Labeling was performed using TextBlob Data Labeling.

## 2. Preprocessing:
There are various procedures involved in preprocessing tweets for sentiment analysis. Any special characters, digits, URLs, and Twitter identities were first removed. Second, to maintain uniformity, all text is changed to lowercase. The tweets are then tokenized, which involves separating them into separate words or tokens. The tokens are then lemmatized to return them to their original forms.

## 3. Feature Extraction:
Feature extraction was used to vectorize data by converting preprocessed text into numerical data using TF-IDF.

## 4. Classification:
Model Selection: Choose suitable classification models for sentiment analysis. For instance, logistic regression, SVM, or neural networks

Training and Testing: Split the dataset into a training set to train the model and a test set to evaluate its performance.

Evaluation: Used metrics like accuracy, precision, recall, and F1-score to measure how well the classifier performs in determining the sentiments of the tweets.

## Results:
Share some insights, metrics, or findings from the analysis. This can be in terms of graphs, tables, or text.

## Technologies Used:
List the languages, libraries, and tools used in the project.

## Contact:
Your contact info or a link to your GitHub profile for those who might have questions or collaboration ideas.
