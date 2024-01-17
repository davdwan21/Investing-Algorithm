import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import ssl
import CountTickers

# disable ssl certificate verification (for some reason the code doesn't run without this line lol)
ssl._create_default_https_context = ssl._create_unverified_context

# download only needs to happen once (already downloaded)
# nltk.download('punkt')
# nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
stock_keywords = ['stock', 'analysis', 'market', 'invest', 'investment']

list_of_urls = []
article_titles = []

def GetArticleUrls():
    # currently only pulls from one website
    url = 'https://www.fool.com/investing-news/'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_divs = soup.find_all('div', class_='flex py-12px text-gray-1100')

    for div in all_divs:
        article_link = div.find('a')

        # href attribute is unique to article links
        article_url = article_link.get('href')

        list_of_urls.append(f'https://www.fool.com{article_url}')

def GetTitle(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        return title
    except Exception as e:
        return f'Error fetching title for {url}: {e}'
    
def IsStockArticle(title):
    # tokenize title for analysis
    words = word_tokenize(title.lower())
    
    # check explicit keywords
    if any(keyword in words for keyword in stock_keywords):
        return True
    else:
        # uses sentiment analysis if no explicit keywords found
        sentiment_score = sia.polarity_scores(title)['compound']
        return sentiment_score >= 0.1


GetArticleUrls()

titles = [GetTitle(url.strip()) for url in list_of_urls]
clean_titles = [title.strip() for title in titles]

for title in clean_titles:
    new_title = title.replace(" | The Motley Fool", "")
    article_titles.append(new_title)

stock_analysis_titles = [title.strip() for title in article_titles if IsStockArticle(title)]

new_urls = []
for i in range(len(list_of_urls)):
    if article_titles[i] in stock_analysis_titles:
        new_urls.append(list_of_urls[i])

with open('article_urls.txt', 'a+') as file:
    for url in new_urls:
        file.write(url + '\n')

CountTickers.Run()