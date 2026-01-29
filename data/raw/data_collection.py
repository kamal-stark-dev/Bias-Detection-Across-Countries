import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# API
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
URL = "https://newsapi.org/v2/everything"

COUNTRY_SOURCES = {
    "India": "the-times-of-india,the-hindu,ndtv",
    "USA": "cnn,abc-news,nbc-news,usa-today",
    # "UK": "bbc-news,the-guardian-uk,independent,sky-news"
    "Australia": "abc-news-au,news-com-au,the-sydney-morning-herald,the-age"
}

TARGET = 1000
PAGE_SIZE = 100

all_headlines = []

for country, sources in COUNTRY_SOURCES.items():
    collected = 0
    end_date = datetime.utcnow()

    print(f"\nCollecting for {country}...")

    while collected < TARGET:
        start_date = end_date - timedelta(days=3)

        params = {
            "apiKey": API_KEY,
            "sources": sources,
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "pageSize": PAGE_SIZE,
            "page": 1,  # free plan safe
            "language": "en",
            "sortBy": "publishedAt"
        }

        response = requests.get(URL, params=params)
        data = response.json()

        if data.get("status") != "ok":
            print(data.get("message"))
            break

        articles = data.get("articles", [])
        if not articles:
            break

        for article in articles:
            title = article.get("title")
            if title:
                all_headlines.append({
                    "headline": title,
                    "country": country,
                    "label": ""
                })
                collected += 1

                if collected >= TARGET:
                    break

        end_date = start_date
        time.sleep(1)

    print(f"Collected {collected} headlines for {country}")

df = pd.DataFrame(all_headlines)
df.drop_duplicates(subset="headline", inplace=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")
df.to_csv(f"headlines_1000_free_plan_{timestamp}.csv", index=False)

print("\nSaved CSV successfully.")
