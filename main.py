import sys
import feedparser
from bs4 import BeautifulSoup
import json

def html_to_json(content, indent=None):
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find_all("tr")

    headers = {}
    thead = True
    data = {}
    for row in rows:
        header = row.find_all("th")[0].text
        item = row.find_all("td")[0].text.replace("\\\"",  "\"")
        data[header] = item
    return data

def save_and_rename(url, title):
    import urllib.request

    response =  urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    url = soup.find_all('meta', {'name':'citation_pdf_url'})[0]['content']

    urllib.request.urlretrieve(url, 'downloads/{}.pdf'.format(title.replace(' ', '_')))

url = sys.argv[1]
feed = feedparser.parse(url)

for entry in feed.entries:
    val = entry['content'][0]['value']
    if 'Comment:' in entry['title']:
        continue
    data = html_to_json(val)
    print(entry['title'])
    print(data['Author'])
    print(data['URL'])
    print(data['Abstract'])
    save_and_rename(data['URL'], entry['title'])
    print()
