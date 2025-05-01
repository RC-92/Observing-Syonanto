# Version Control/
## version 2: SammyBoy Scraper - Fix to contentRow-title, username, u-dt

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Settings
URL = "https://www.sammyboy.com/whats-new/latest-activity"

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Your Chromium path
    chrome_options.binary_location = "/usr/bin/chromium-browser"

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def load_sammyboy(driver):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Going to URL...")
    driver.get(URL)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] URL Loaded.")

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "block-container"))
        )
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Block container (table area) found!")
    except Exception as e:
        print(f"[ERROR] Block container not found within timeout. {e}")
        return

    # Now find all posts by contentRow-title
    threads = driver.find_elements(By.CLASS_NAME, "contentRow-title")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Found {len(threads)} posts.")

    for idx, title_element in enumerate(threads, start=1):
        try:
            # Title Text and Link
            title_text = title_element.text.strip()
            title_link = title_element.find_element(By.TAG_NAME, "a").get_attribute("href")

            # Get the parent row (move upward) to find username and time
            parent_row = title_element.find_element(By.XPATH, "../../..")

            # Username
            username_element = parent_row.find_element(By.CLASS_NAME, "username")
            username_text = username_element.text.strip()

            # Time
            time_element = parent_row.find_element(By.CLASS_NAME, "u-dt")
            time_text = time_element.get_attribute("title")

            print(f"{idx}. Title: {title_text}")
            print(f"   Link: {title_link}")
            print(f"   Time: {time_text}")
            print(f"   Username: {username_text}")
            print("-" * 60)

        except Exception as e:
            print(f"[WARNING] Could not extract a post properly: {e}")

if __name__ == "__main__":
    driver = setup_browser()
    try:
        load_sammyboy(driver)
    finally:
        driver.quit()

