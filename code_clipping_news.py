import requests
from bs4 import BeautifulSoup
import pyshorteners

# URL shortening function
def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

def scrape_news_itatiaia(url,n):
    position = url.find('.br')+3
    cropped_url = url[:position]
    # Send a GET request to the website
    response = requests.get(url)
    # Ensure the correct encoding is used based on the webpage's content type
    if response.encoding is None or response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    news_links = soup.find_all('div', class_='PagePromo-title', limit=n) # find n divs with class 'PagePromo-title'
    news_data = []
   # Prepare a list to store tuples of (title, link)
    for link in news_links:
        # Check if it is a children of the main news div, defined by classes 'PageListStandardC"' or 'PageListStandardB' depending on the page
        if link.find_parent(class_ = "PageListStandardC") or link.find_parent(class_ = "PageListStandardB"):
            href = link.a.get("href") # Extract the URL from the 'href' attribute
            title = link.a.string # Extract title from the 'a' tag
            # Check if the link is relative and prepend the base URL if needed
            if href and href.startswith('/'):
                href = cropped_url + href # Append the base domain to the relative URL 
            # Append the tuple (title, href) to the list
            news_data.append((title, href))
    return news_data

def gather_news_itatiaia(fonte_noticias,n):
    all_news = {}
    for url, category in fonte_noticias.items():
        news = scrape_news_itatiaia(url,n)
        if category not in all_news:
            all_news[category] = []
        all_news[category].extend(news)
    return all_news

def format_news(all_news):
    # Format news text
    news_text = ""
    for category, items in all_news.items():
        news_text += f"📌 {category.title()}:\n"
        for title, link in items:
            short_link = shorten_url(link)
            news_text += f"📰 {title}: {short_link}\n"
        news_text += "\n"

    return news_text

    

if __name__ == "__main__":

    from datetime import datetime
    from tqdm import tqdm

    new_sources_itatiaia ={
        'https://www.itatiaia.com.br/politica':'Política',
        'https://www.itatiaia.com.br/economia':'Economia'
    }
    # get user's input
    n = int(input("quantas noticias gostaria de ver? "))
    all_news = gather_news_itatiaia(new_sources_itatiaia,n)
    
    news_text = format_news(all_news)
    print(news_text)