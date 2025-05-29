from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv, datetime, time, os, pickle

CSV_FILE = "snek_captions.csv"
COOKIE_FILE = "cookies.pkl"
IMAGE_FOLDER = "images"
TWITTER_URL = "https://twitter.com/compose/tweet"
OPENSEA_CONTRACT = "0x22b0414cce0593ee1a87d83f91f569d505de9160"

# Set up headless Chrome
options = Options()
options.binary_location = "/usr/bin/chromium-browser"
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://twitter.com")  # Visit domain before setting cookies

# Load cookies
if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)

    for i, cookie in enumerate(cookies):
        name = cookie.get("name", "unknown")
        same_site = cookie.get("sameSite", "")
        normalized = same_site.capitalize() if isinstance(same_site, str) else ""

        if normalized not in ["Strict", "Lax", "None"]:
            print(f"⚠️ Skipping cookie #{i+1} ('{name}') due to invalid sameSite='{same_site}'")
            continue

        cookie["sameSite"] = normalized
        try:
            driver.add_cookie(cookie)
            print(f"✅ Added cookie #{i+1} '{name}'")
        except Exception as e:
            print(f"❌ Failed to add cookie #{i+1}: {e}")

    driver.get(TWITTER_URL)
else:
    print("❌ cookies.pkl not found.")
    driver.quit()
    exit()

# Wait for the tweet box
try:
    tweet_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']"))
    )
except Exception:
    print("❌ Tweet failed: Could not find tweet input box.")
    driver.save_screenshot("debug_tweet_page.png")
    with open("debug_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    driver.quit()
    exit()

# Get today's tweet
today = datetime.datetime.utcnow().strftime('%b %d, %Y')
with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['date'].strip() == today:
            caption = row['caption']
            file_name = row['file_name']
            token_id = file_name.replace("snek_", "").replace(".png", "")
            image_path = os.path.join(IMAGE_FOLDER, file_name)

            tweet_text = f"{caption}\nhttps://opensea.io/assets/base/{OPENSEA_CONTRACT}/{token_id}"
            print("Tweet text to be sent:", tweet_text)

            try:
                tweet_box.send_keys(tweet_text)
                time.sleep(2)

                file_input = driver.find_element(By.XPATH, "//input[@type='file']")
                file_input.send_keys(os.path.abspath(image_path))
                time.sleep(4)

                # Wait for tweet button and click
                post_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButtonInline']"))
                )
                post_button.click()
                print("✅ Tweet posted.")

            except Exception as e:
                print(f"❌ Tweet failed during post: {e}")
                driver.save_screenshot("tweet_fail.png")
            break

driver.quit()
