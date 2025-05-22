# tweet_snek.py
import os
import csv
import datetime
import tweepy

# Set up Twitter auth from environment
auth = tweepy.OAuth1UserHandler(
    os.environ['TWITTER_API_KEY'],
    os.environ['TWITTER_API_SECRET'],
    os.environ['TWITTER_ACCESS_TOKEN'],
    os.environ['TWITTER_ACCESS_SECRET']
)
api = tweepy.API(auth)

# Get today's date in the format used in the CSV
today = datetime.datetime.utcnow().strftime('%b %d, %Y')
print(f"Today's date is: {today}")

# Read the CSV
with open('snek_captions.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(f"Checking row with date: {row['date']}")
        if row['date'].strip() == today:
            caption = row['caption']
            image_path = os.path.join('images', row['file_name'])
            print(f"Posting {image_path} with caption: {caption}")
            try:
                media = api.media_upload(image_path)
                api.update_status(status=caption, media_ids=[media.media_id])
                print("Tweet posted successfully.")
            except Exception as e:
                print("Twitter post failed:", e)
            break
    else:
        print(f"No Snek scheduled for today ({today})")
