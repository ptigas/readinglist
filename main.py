import sys
import feedparser
from bs4 import BeautifulSoup
import json
import glob

import os
import smtplib, ssl


DOWNLOADS_DIR = sys.argv[1]
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# get key
with open('zotero_feed') as f:
   url = f.read()

mem = {}
for f in glob.glob(DOWNLOADS_DIR + "/*.pdf"):
    key = f.split(DOWNLOADS_DIR + "/")[1].split(".pdf")[0]
    mem[key] = f

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
    if not '.pdf' in url:
        req = urllib.request.Request(url, headers=headers)
        response =  urllib.request.urlopen(req)
        soup = BeautifulSoup(response, 'html.parser')
        url = soup.find_all('meta', {'name':'citation_pdf_url'})[0]['content']
        print('{} - done'.format(title))

    urllib.request.urlretrieve(url, DOWNLOADS_DIR + '/{}.pdf'.format(title.replace(' ', '_')))

feed = feedparser.parse(url)

for entry in feed.entries:
    val = entry['content'][0]['value']
    if 'Comment:' in entry['title']:
        continue
    if entry['title'].replace(' ', '_') in mem:
        continue
    data = html_to_json(val)
    try:
        save_and_rename(data['URL'], entry['title'])
    except Exception as e:
        print(e)
