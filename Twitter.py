import tweepy as tw  # To connect to the API and to collect the data we needed 
import pandas as pd  # To store the Twitter data into a file just in case for further use
from matplotlib import pyplot as plt
import seaborn as sns # Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics.
import collections
import nltk  # Natural language processing (NLP) is a field that focuses on making natural human language usable by computer programs
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from tabulate import tabulate
from wordcloud import WordCloud, STOPWORDS

sns.set(font_scale=1.5)
sns.set_style("whitegrid")

# We need to define our credentials
api_key = 'YOUR_KEY'
api_secret_key = 'YOUR_SECRET_KEY'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'TOUR_ACCESS_TOKEN_SECRET'
# Authentication
auth = tw.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

search_word = "Elon Musk+Tesla"
sv = search_word.lower()
sv = sv.replace("+", " ")
sv = sv.split()


 # Scrape the Twitter data
def scrapData():
    auth = tw.OAuthHandler(api_key, api_secret_key)
    api = tw.API (auth, wait_on_rate_limit=True) 
    tweets = tw.Cursor(api.search_tweets, q = search_word, lang ='en').items(1000) # We grab 1000 recent tweets and add them to a list
    all_tweets = [tweet.text for tweet in tweets]
    return all_tweets


def save_to_file(location, name, file):
    f = open(location + "/" + name, "w", encoding="utf-8")
    f.writelines(file)
    f.close()

#newSearch = scrapData("Elon Musk+Tesla")
#save_to_file("C:/Users/minic/OneDrive/Радна површина", "ElonMuskTesla.txt", newSearch)
l = open("C:/Users/minic/OneDrive/Радна површина/ElonMuskTesla.txt","r",  encoding="utf-8")
txt = l.read()
#print(txt)

def cleaning(txt):
    txt= re.sub(r"http[s]\S+", " ", txt) # Removing URLs from tweets 
    txt= re.sub(r"rt[\s]+", " ", txt)   # Removing old style retweet text "RT"
    txt=re.sub(r"(@[A-Za-z0–9_]+)|[^\w\s]|#|http\S+", "", txt)   # Removing links, hash characters, and punctuation   
    txt = txt.lower()   # Creating each word lowercase
    txt=txt.replace ("hes"," ") 
    txt=txt.replace ("intrt", " ")
    txt=txt.replace ("musks", " ")
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(txt)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    filtered_sentence = []
 
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    res = filter(lambda i: i not in sv, filtered_sentence)
    return list(res)


cleaned_txt=cleaning(txt)  # Calling the function and named as cleaned_txt
#print(cleaned_txt)


counts_of_words = collections.Counter(cleaned_txt) # Creating a counter
most_common= counts_of_words.most_common(11)
#print(most_common)

df= pd.DataFrame (most_common, columns=["word", "count"])    # Arranging data in a table
table= tabulate(df, headers=["word", "count"], tablefmt= "grid")
#print (table)

#df.to_csv('C:/Users/minic/OneDrive/Радна површина/HI/4. Python module/Excercise/DataFrame.csv', index = False, encoding='utf-8') # Saving the most common words into csv file
#print(df)


fig, ax = plt.subplots(figsize=(12,3))   # Visualization --> BarChart
df.sort_values (by="count").plot.barh(x="word", y="count", title="Most common words in Tweets", ax=ax, color="red")
plt.show()



string = pd.Series(cleaned_txt).str.cat(sep=' ')  # Visualization --> WordCloud
stopwords = set(STOPWORDS)
stopwords.update(["elonmusk","elon musk","elon","musk","tesla", "musks", "hes", "intrt", "teslas"]) #adding our own stopwords
wordcloud = WordCloud(width=1600, stopwords=stopwords,height=800,max_font_size=200,max_words=50,collocations=False, background_color='black').generate(string)
plt.figure(figsize=(40,30))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()