import os
import csv
import datetime
import tweepy

# Auth for v2 (Bearer Token required)
client = tweepy.Client(
    consumer_key=os.environ['TWITTER_API_KEY'],
    consumer_secret=os.environ['TWITTER_API_SECRET'],
    access_token=os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret=os.environ['TWITTER_ACCESS_SECRET']
)

# Format today's date to match CSV (e.g., "May 22, 2025")
today = datetime.datetime.utcnow().strftime('%b %d, %Y')

# Your Base contract address
contract = "0x22b0414cce0593ee1a87d83f91f569d505de9160"

# Open CSV and look for today's Snek
with open("snek_captions.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["date"].strip() == today:
            caption = row["caption"]
            file_name = row["file_name"]  # e.g., snek_114.png
            token_id = file_name.replace("snek_", "").replace(".png", "")
            opensea_url = f"https://opensea.io/item/base/{contract}/{token_id}"
            tweet_text = f"{caption}\n{opensea_url}"
            try:
                client.create_tweet(text=tweet_text)
                print("✅ Tweet posted successfully.")
            except Exception as e:
                print("❌ Twitter post failed:", e)
            break
    else:
        print("⚠️ No tweet scheduled for today.")

