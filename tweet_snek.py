import tweepy
import csv
import datetime
import os

# Auth
auth = tweepy.OAuth1UserHandler(
    os.environ['TWITTER_API_KEY'],
    os.environ['TWITTER_API_SECRET'],
    os.environ['TWITTER_ACCESS_TOKEN'],
    os.environ['TWITTER_ACCESS_SECRET']
)

api = tweepy.API(auth)

# Get today’s date formatted like "May 22, 2025"
today = datetime.datetime.utcnow().strftime('%b %d, %Y')

# Read the CSV and find the row matching today's date
with open('snek_captions.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['date'] == today:
            caption = row['caption']
            token_id = row['file_name'].split('_')[1].split('.')[0]
            token_url = f"https://opensea.io/assets/base/0x22b0414cce0593ee1a87d83f91f569d505de9160/{token_id}"
            tweet_text = f"{caption}\n{token_url}"
            api.update_status(status=tweet_text)
            break
