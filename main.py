import sys
import feedparser
from bs4 import BeautifulSoup
import json
import glob

import os
import smtplib, ssl

os.makedirs(sys.argv[2], exist_ok=True)

mem = {}
for f in glob.glob(sys.argv[2] + "/*.pdf"):
    key = f.split(sys.argv[2] + "/")[1].split(".pdf")[0]
    mem[key] = f
    print(key)

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

    headers = {'User-Agent': 'Mozilla/5.0'}
    if '.pdf' not in url:
        req = urllib.request.Request(url, headers=headers)
        response =  urllib.request.urlopen(req)
        soup = BeautifulSoup(response, 'html.parser')
        url = soup.find_all('meta', {'name':'citation_pdf_url'})[0]['content']
        print('{} - done'.format(title))

    urllib.request.urlretrieve(url, sys.argv[2] + '/{}.pdf'.format(title.replace(' ', '_')))

url = sys.argv[1]
feed = feedparser.parse(url)

for entry in feed.entries:
    val = entry['content'][0]['value']
    if 'Comment:' in entry['title']:
        continue
    if entry['title'].replace(' ', '_') in mem:
        continue
    data = html_to_json(val)
    '''
    print(data['Abstract'])
    '''
    try:
        save_and_rename(data['URL'], entry['title'])
    except Exception as e:
        pass
