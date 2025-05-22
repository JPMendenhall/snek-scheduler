import os
import csv
import datetime
import tweepy

# Twitter auth
auth = tweepy.OAuth1UserHandler(
    os.environ['TWITTER_API_KEY'],
    os.environ['TWITTER_API_SECRET'],
    os.environ['TWITTER_ACCESS_TOKEN'],
    os.environ['TWITTER_ACCESS_SECRET']
)
api = tweepy.API(auth)

# Today's date format (e.g., "May 17, 2025")
today = datetime.datetime.utcnow().strftime('%b %d, %Y')
print(f"Today's date is: {today}")

# Contract address for Sneks
contract_address = "0x22b0414cce0593ee1a87d83f91f569d505de9160"

# Find today's row
with open('snek_captions.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['date'].strip() == today:
            caption = row['caption']
            file_name = row['file_name']  # e.g., snek_114.png
            token_id = file_name.replace("snek_", "").replace(".png", "")
            url = f"https://opensea.io/item/base/{contract_address}/{token_id}"
            full_tweet = f"{caption}\n{url}"
            try:
                api.update_status(full_tweet)
                print("✅ Tweet posted successfully.")
            except Exception as e:
                print("❌ Twitter post failed:", e)
            break
    else:
        print(f"No Snek scheduled for today ({today})")
