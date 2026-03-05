import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# create articles folder if not exists
os.makedirs("articles", exist_ok=True)

# read input file
df = pd.read_excel("Input.xlsx")

for index, row in df.iterrows():

    url_id = row['URL_ID']
    url = row['URL']

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # extract title
        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else ""

        # extract article paragraphs
        paragraphs = soup.find_all('p')

        article_text = ""
        for p in paragraphs:
            article_text += p.get_text() + "\n"

        full_text = title_text + "\n\n" + article_text

        # save article
        with open(f"articles/{url_id}.txt", "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"Saved article {url_id}")

    except Exception as e:
        print(f"Error with {url_id}: {e}")