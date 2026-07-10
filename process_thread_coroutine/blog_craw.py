import requests
from bs4 import BeautifulSoup

urls = [
    f"https://www.cnblogs.com/cate/4/#p{page}"
    for page in range(1,51)
]

def craw(url):
    r = requests.get(url)
    # print(url,len(r.text)) 
    return r.text

def parse(html):
    soup = BeautifulSoup(html,"html.parser")
    links = soup.find_all("a",class_ = "post-item-title")
    return [(link["href"],link.get_text()) for link in links]
