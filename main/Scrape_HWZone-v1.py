# Version Control/
## version 5: Scrape structItem-title, u-dt, username

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Settings
URL = "https://forums.hardwarezone.com.sg/whats-new/posts/4185101"

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Your Chromium path
    chrome_options.binary_location = "/usr/bin/chromium-browser"

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def load_hwz(driver):
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

    # Now find all posts
    threads = driver.find_elements(By.CLASS_NAME, "structItem--thread")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Found {len(threads)} threads.")

    for idx, thread in enumerate(threads, start=1):
        try:
            # Extract title
            title_element = thread.find_element(By.CLASS_NAME, "structItem-title")
            title_text = title_element.text.strip()
            title_link = title_element.find_element(By.TAG_NAME, "a").get_attribute("href")

            # Extract timestamp
            time_element = thread.find_element(By.CLASS_NAME, "u-dt")
            time_text = time_element.get_attribute("title")

            # Extract username
            username_element = thread.find_element(By.CLASS_NAME, "username")
            username_text = username_element.text.strip()

            print(f"{idx}. Title: {title_text}")
            print(f"   Link: {title_link}")
            print(f"   Time: {time_text}")
            print(f"   Username: {username_text}")
            print("-" * 60)

        except Exception as e:
            print(f"[WARNING] Could not extract a thread properly: {e}")

if __name__ == "__main__":
    driver = setup_browser()
    try:
        load_hwz(driver)
    finally:
        driver.quit()

