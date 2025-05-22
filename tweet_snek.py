import os
import csv
import datetime
import tweepy

# OAuth 1.0a (v1.1-compatible) – use your existing tokens
auth = tweepy.OAuth1UserHandler(
    os.environ["TWITTER_API_KEY"],
    os.environ["TWITTER_API_SECRET"],
    os.environ["TWITTER_ACCESS_TOKEN"],
    os.environ["TWITTER_ACCESS_SECRET"]
)

api = tweepy.API(auth)

# Format date
today = datetime.datetime.utcnow().strftime('%b %d, %Y')

contract = "0x22b0414cce0593ee1a87d83f91f569d505de9160"

# Read today's Snek from CSV
with open("snek_captions.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["date"].strip() == today:
            caption = row["caption"]
            file_name = row["file_name"]
            token_id = file_name.replace("snek_", "").replace(".png", "")
            opensea_url = f"https://opensea.io/item/base/{contract}/{token_id}"
            tweet = f"{caption}\n{opensea_url}"
            try:
                api.update_status(tweet)
                print("✅ Tweet sent.")
            except Exception as e:
                print("❌ Twitter post failed:", e)
            break
    else:
        print("⚠️ No matching date in CSV.")
