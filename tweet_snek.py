from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv, datetime, time, os, pickle

CSV_FILE = "snek_captions.csv"
COOKIE_FILE = "cookies.pkl"
TWITTER_URL = "https://twitter.com/compose/tweet"
OPENSEA_CONTRACT = "0x22b0414cce0593ee1a87d83f91f569d505de9160"

# Headless browser config
options = Options()
options.binary_location = "/usr/bin/chromium-browser"
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(options=options)
driver.get("https://twitter.com/login")

# Load cookies
if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)

    for i, cookie in enumerate(cookies):
        name = cookie.get("name", "unknown")
        original_same_site = cookie.get("sameSite", "")
        normalized = original_same_site.capitalize()

        # Fix or skip invalid sameSite values
        if normalized not in ["Strict", "Lax", "None"]:
            print(f"⚠️ Skipping cookie #{i+1} ('{name}') due to invalid sameSite='{original_same_site}'")
            continue
        cookie["sameSite"] = normalized

        try:
            driver.add_cookie(cookie)
            print(f"✅ Added cookie #{i+1} '{name}' with sameSite='{cookie['sameSite']}'")
        except Exception as e:
            print(f"❌ Failed to add cookie #{i+1} '{name}': {e}")
    driver.get(TWITTER_URL)
else:
    print("❌ cookies.pkl not found.")
    driver.quit()
    exit()


# Get today's tweet
today = datetime.datetime.utcnow().strftime('%b %d, %Y')
with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['date'].strip() == today:
            caption = row['caption']
            token_id = row['file_name'].replace("snek_", "").replace(".png", "")
            tweet_text = f"{caption}\nhttps://opensea.io/assets/base/{OPENSEA_CONTRACT}/{token_id}"

            # Post
            try:
                time.sleep(5)
                box = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Tweet text']")
                box.send_keys(tweet_text)
                time.sleep(2)
                post_button = driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']")
                post_button.click()
                print("✅ Tweet posted.")
            except Exception as e:
                print(f"❌ Tweet failed: {e}")
            break

driver.quit()
