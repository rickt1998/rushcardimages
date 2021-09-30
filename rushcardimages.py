import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Use sheet as database because still no up-to-date endpoint (lmao)
sheet_id = "1LmaojiWWhDxuKO8kFNfGH7tCOO5fuy4hjAC5WNDN4gg"
sheet_name = "Sheet1"
sheeturl = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(sheeturl)
df.columns = ['edoproid', 'edoproname', 'omegaid', 'omeganame']

processed = set()


def download(url, type):
    response = requests.get(url)
    if response.ok:
        # Scrape 1024x1024 image url from wiki
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.findAll('div', id='file')[0]
        if type == 'cardart':
            imgurl = div.findAll('img')[0]['srcset'].split(' ')[2]
        elif type == 'hologram':
            imgurl = div.findAll('img')[0]['src']
        img = requests.get(imgurl)

        # Write to file with cardid
        _dir = f"./{type}/{cardid}.png"
        file = open(_dir, "wb")
        file.write(img.content)
        file.close()

        # Add to list to ignore alt arts
        processed.add(wikiname)


for cardname, cardid in zip(df['omeganame'], df['omegaid']):
    # Strip special chars
    wikiname = re.sub('[^A-Za-z0-9]+', '', cardname)
    if wikiname not in processed:
        print(cardname)
        arturl = f"https://yugipedia.com/wiki/File:{wikiname}-SBR-JP-VG-artwork.png"
        holourl = f"https://yugipedia.com/wiki/File:{wikiname}-SBR-JP-VG-NC.png"
        download(arturl, 'cardart')
        download(holourl, 'hologram')
