from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def extract_facebook_posts(url, limit=5):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    browser = webdriver.Chrome(options=options)

    with open("facebook_posts.jsonl", "w", encoding="utf-8") as out:
        try:
            browser.get(url)
            time.sleep(5)

            try:
                btn = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@aria-label, 'Close') or contains(@aria-label, 'Закрити')]"))
                )
                btn.click()
                time.sleep(2)
            except:
                pass

            for _ in range(3):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

            posts = browser.find_elements(By.XPATH, "//div[contains(@class, 'x1yztbdb')]")

            for idx, el in enumerate(posts[:limit]):
                post_info = {"post_url": "Not found", "content": "Not found", "date": "Not found"}

                try:
                    url_el = el.find_element(By.XPATH, ".//a[contains(@href, '/posts/')]")
                    post_info["post_url"] = url_el.get_attribute("href").split('?')[0]
                except:
                    pass

                try:
                    txt_el = el.find_element(By.XPATH, ".//div[@data-ad-comet-preview='message']//div[@dir='auto']")
                    post_info["content"] = txt_el.text.strip()
                except:
                    pass

                try:
                    date_el = el.find_element(By.XPATH, ".//span[contains(@class, 'x4k7w5x')]")
                    post_info["date"] = date_el.text.strip()
                except:
                    pass

                json.dump(post_info, out, ensure_ascii=False)
                out.write("\n")

        finally:
            browser.quit()

target_url = "https://www.facebook.com/providentrealestateuz"
extract_facebook_posts(target_url)