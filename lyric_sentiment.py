'''
LYRIC SENTIMENT ANALYSIS
- Scrap Lyrics from AZLyrics and analyze most common topics, most common words, and positivity / negativity
'''

'''
IMPORT STATEMENT
- Importing selenium, beautiful soup, requests for website scrapping
- Pandas for data cleaning and analysis
'''
# For GUI Modules
import tkinter as tk
from PIL import Image, ImageTk 

from bs4 import BeautifulSoup
import requests
from nltk.tokenize import word_tokenize
from stop_words import get_stop_words
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

'''
FUNCTION TO GENERATE SENTIMENT FROM URL
'''
def get_lyric_info():

    '''
    IMPORTING SONG LYRICS FROM WEB SCRAPPING
    '''
    # Getting URL of Song as Input
    url = str(url_entry.get())
    response = requests.get(url)

    # Cleaning Up Song Lyrics Inputs
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finding the div class of the lyrics of the song
    page = soup.find('div', {'class':"col-xs-12 col-lg-8 text-center"})
    children = page.findChildren("div" , recursive=False)

    # 4th Child of the DIV Class has Lyrics for AZLyrics Website
    lyric = children[4]

    # Cleaning Lyrics of the Tags
    lyric = lyric.text

    '''
    NATURAL LANGUAGE PROCESSING - USING NLTK
    - Cleaning Stop Words like (you, me, to, etc)
    '''

    # Defining Stop Words
    stopwords = list(get_stop_words('en'))   
    word_tokens = word_tokenize(lyric)

    # Removing ' from word tokens
    word_tokens = list(word_tokens)
    new_word_tokens = []
    for i in range(0,len(word_tokens)):
        if "'" in word_tokens[i]:
            try:
                del new_word_tokens[-1] 
            except:
                continue
        else:
            new_word_tokens.append(word_tokens[i].lower())

    # Defining the list for filtered lyrics
    filtered_lyric = []
    
    # Seperating Lyrics with and without Stop Words
    for w in new_word_tokens:
        if w not in stopwords:
            filtered_lyric.append(w.lower())

    ''' 
    DATA ANALYSIS OF SONG 
    - Most common words 
    - Positivity and Negativity Analysis
    '''

    word_count = {}
    # Getting Word Count of Each Word
    for words in filtered_lyric:
        if words in word_count.keys():
            word_count[words] += 1
        else:
            word_count[words] = 1

    # Removing one character words
    clean_word_counts = {}
    for keys in word_count.keys():
        if len(keys) > 1:
            clean_word_counts[keys] = word_count[keys]
            
    # Sorting by Most Common Words
    sorted_dict = {}
    sorted_keys = sorted(clean_word_counts, key=clean_word_counts.get)

    for w in sorted_keys:
        sorted_dict[w] = clean_word_counts[w]

    # Untokenizing Words
    tokened_words = ''
    tokened_words += " ".join(filtered_lyric)+" "

    # Creating Word Cloud
    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 10).generate(tokened_words)

    # Plot Word Cloud Image                   
    plt.figure(figsize = (16, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)

    # Save Word Cloud Image
    plt.savefig('wordcloud.png', dpi = 28)

    # Sentiment Analysis 
    blob = TextBlob(lyric)
    sentiment = blob.sentiment.polarity 
    sentiment_score = round(sentiment,2)

    # Putting Sentiment Score into Human Terms
    sentiment_explained = ""
    if sentiment_score > 0:
        if sentiment_score > 0.5:
            sentiment_explained = "This is a very positive song with a score of " + str(sentiment_score)
        else:
            sentiment_explained = "This is a slightly positive song with a score of " + str(sentiment_score)
    else:
        if sentiment_score < -0.5:
            sentiment_explained = "This is a very negative song with a score of " + str(sentiment_score)
        else:
            sentiment_explained = "This is a slightly negative song with a score of " + str(sentiment_score)

    '''
    Generate Word Cloud Image
    '''
    # Import Previously Created Word Cloud
    wordcloud = Image.open('wordcloud.png')
    wordcloud = ImageTk.PhotoImage(wordcloud)
    wordcloud_label = tk.Label(image = wordcloud)
    wordcloud_label.image = wordcloud
    wordcloud_label.place(x = 700, y = 350)
    
    
    # Inserting Sentiment Score Into Text Box
    text_box.delete('1.0',tk.END)
    text_box.insert(tk.END, sentiment_explained)
    
'''
Setting Up Tkinter Object for GUI
'''
# Setting Up Tkinter Object
root = tk.Tk()
root.title("Lyric Sentiment Analysis")

# Setting Up the Canvas
canvas = tk.Canvas(root, width = 1494, height = 840)
canvas.grid(columnspan=20, rowspan = 20)

# Importing Image
background = Image.open('background_resize.png')
background = ImageTk.PhotoImage(background)
background_label = tk.Label(image = background)
background_label.image = background
background_label.grid(column = 10, row = 10)

# Creating Input Field on Canvas
url_entry = tk.Entry(root, font=('Raleway 11'))
canvas.create_window(850, 175, height = 50, width = 300, window = url_entry)

# Creating Button to Generate Sentiment Analysis and Webscraping
btn = tk.Button(root, text = "Generate", font = "Raleway", command = get_lyric_info)
btn.place(x = 1100, y = 150, in_=root)

# Creating Text Object for Sentiment Score
text_box = tk.Text(root, height = 2, width = 50, font=('Raleway 11'))
text_box.place(x = 700, y = 690, in_=root)

root.mainloop()