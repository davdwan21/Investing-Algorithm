import requests
import re
from bs4 import BeautifulSoup
from collections import Counter
import json

# creates ticker_dict from json file, a dictionary with all stock tickers as values
with open('tickers.json', 'r') as ticker_file:
    data = json.load(ticker_file)

target_key = 'ticker'
ticker_dict = {}
i = 0

for k, nested_dict in data.items():
    if target_key in nested_dict:
        ticker_dict[i] = nested_dict.get(target_key, None)
        i += 1

with open('tickers.txt', 'r') as f:
    f.read()
    
def GetTextFromUrl(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        return text_content
    else:
        print(f"Error: {response.status_code}")
        return None

url_list = []

# use testing.txt for testing
# use article_urls.txt for actual runs
with open('testing.txt', 'r') as file:
    url_list = file.read().splitlines()

remove_acronyms = []
with open('remove_acronyms.txt', 'r') as file:
    remove_acronyms = file.read().splitlines()

pattern = re.compile(r'\b[A-Z]{2,5}\b')

all_tickers = []

for url in url_list:
    web_text = GetTextFromUrl(url)
    tickers = re.findall(pattern, web_text)
    tck = set(tickers)
    all_tickers.extend(tck)
    
filtered_tickers = [ticker for ticker in all_tickers if ticker in ticker_dict.values()]

ticker_count = Counter(filtered_tickers)
sorted_tickers = ticker_count.most_common()

for key, value in sorted_tickers:
    print(f"{key}: {value}")
