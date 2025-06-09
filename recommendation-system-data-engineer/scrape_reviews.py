from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import re
import random
import os
from datetime import datetime

def random_sleep(base=1, variance=0.5):
    sleep_time = base + random.uniform(0, variance)
    time.sleep(sleep_time)
    return sleep_time

def check_for_captcha(driver):
    try:
        captcha_indicators = [
            "//div[contains(text(), 'CAPTCHA')]",
            "//iframe[contains(@src, 'recaptcha')]",
            "//div[@class='g-recaptcha']",
            "//div[contains(@class, 'captcha')]",
        ]
        for indicator in captcha_indicators:
            elements = driver.find_elements(By.XPATH, indicator)
            if elements and any(elem.is_displayed() for elem in elements):
                print("⚠️ CAPTCHA detected! Please solve it manually in the browser window.")
                input("Press Enter after solving the CAPTCHA to continue...")
                return True
        return False
    except:
        return False

def find_clickable_element(driver, selectors):
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed():
                    return element
        except:
            continue
    return None

def extract_text_from_element(container, selectors):
    for selector in selectors:
        try:
            elements = container.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed() and element.text:
                    return element.text
        except:
            continue
    return ""

def extract_rating(card):
    try:
        rating_elements = card.find_elements(By.CSS_SELECTOR, "[aria-label*='bintang'], [aria-label*='star']")
        for elem in rating_elements:
            aria_label = elem.get_attribute("aria-label")
            if aria_label:
                rating_match = re.search(r'(\d+(?:,\d+)?)\s*(?:bintang|stars?|★)', aria_label)
                if rating_match:
                    return rating_match.group(1).replace(",", ".")
    except:
        pass
    
    try:
        filled_stars = card.find_elements(By.CSS_SELECTOR, ".vzX5Ic[aria-hidden='true'], .RVQdVd")
        if filled_stars:
            return str(len(filled_stars))
    except:
        pass
    
    return ""

def main():
    MAX_REVIEWS = 10
    output_folder = "google_maps_reviews"
    os.makedirs(output_folder, exist_ok=True)
    
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=id")
    
    temp_dir = os.path.join(os.getcwd(), "chrome_temp_data")
    os.makedirs(temp_dir, exist_ok=True)
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    try:
        os.system("taskkill /f /im chrome.exe")
        time.sleep(2)
    except:
        pass
    
    options.add_argument("--remote-debugging-port=9222")
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['id-ID', 'id', 'en-US', 'en']
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """
    })
    
    place_url = "https://www.google.com/maps/place/Amanah+Agrotourism/@-7.6335166,111.0964229,14.67z/data=!4m22!1m12!3m11!1s0x2e798a3abfb68e99:0x8971ae316670f346!2sAmanah+Agrotourism!5m2!4m1!1i2!8m2!3d-7.6318197!4d111.1062169!9m1!1b1!16s%2Fg%2F1pzqn94mj!3m8!1s0x2e798a3abfb68e99:0x8971ae316670f346!5m2!4m1!1i2!8m2!3d-7.6318197!4d111.1062169!16s%2Fg%2F1pzqn94mj?entry=ttu&g_ep=EgoyMDI1MDUyNy4wIKXMDSoASAFQAw%3D%3D"
    driver.get(place_url)
    print(f"Opening page: {place_url}")
    random_sleep(5, 2)
    
    check_for_captcha(driver)
    
    review_button_selectors = [
        'button[jsaction*="pane.reviewChart.moreReviews"]',
        'button[aria-label*="ulasan"]', 
        'button[aria-label*="review"]',
        'div.F7nice button'
    ]
    
    review_button = find_clickable_element(driver, review_button_selectors)
    if review_button:
        driver.execute_script("arguments[0].click();", review_button)
        print("Review button clicked")
        random_sleep(3, 1)
    else:
        panel_selectors = [
            'div.F7nice', 
            'div[jsaction*="pane.rating.moreReviews"]', 
            'span[aria-label*="bintang"]', 
            'span[aria-label*="star"]'
        ]
        panel = find_clickable_element(driver, panel_selectors)
        if panel:
            driver.execute_script("arguments[0].click();", panel)
            print("Rating panel clicked")
            random_sleep(3, 1)
    
    scroll_selectors = [
        'div[aria-label*="Ulasan"]',
        'div.m6QErb.DxyBCb.kA9KIf.dS8AEf',
        'div[role="feed"]'
    ]
    
    scrollable_div = None
    for selector in scroll_selectors:
        try:
            scrollable_div = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            print(f"Found scrollable container with selector: {selector}")
            break
        except TimeoutException:
            print(f"Timeout waiting for scrollable container with selector: {selector}")
    
    if not scrollable_div:
        # Save HTML for debugging
        with open("page_source_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Page source saved to page_source_debug.html")
        raise Exception("Could not find scrollable container")
    
    try:
        sort_selectors = ['button[aria-label*="Sortir"], button[aria-label*="sort"]']
        sort_button = find_clickable_element(driver, sort_selectors)
        if sort_button:
            driver.execute_script("arguments[0].click();", sort_button)
            random_sleep(2, 1)
            
            newest_selectors = ['div[role="menuitem"], div[role="option"]']
            newest_option = find_clickable_element(driver, newest_selectors)
            if newest_option and ("Terbaru" in newest_option.text or "Newest" in newest_option.text):
                driver.execute_script("arguments[0].click();", newest_option)
                print("Sorted by newest")
                random_sleep(3, 1)
    except:
        print("Could not sort reviews")
    
    print("Scrolling to load more reviews...")
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    scrolls = 0
    reviews_before = 0
    no_new_reviews_count = 0
    consecutive_same_height = 0
    
    # Try to force load additional reviews with various techniques
    force_loading_techniques = [
        # Technique 1: Scroll to top and back to bottom
        lambda: (
            driver.execute_script("arguments[0].scrollTop = 0", scrollable_div),
            random_sleep(1, 0.5),
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        ),
        # Technique 2: Scroll to middle and back to bottom
        lambda: (
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight / 2", scrollable_div),
            random_sleep(1, 0.5),
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        ),
        # Technique 3: Click on a review and back to scrolling
        lambda: try_click_review_and_back(driver, scrollable_div)
    ]
    
    while True:
        if scrolls % 5 == 0:
            check_for_captcha(driver)
        
        current_reviews = len(driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf, div[jscontroller="e6Mltc"]'))
        
        if current_reviews >= MAX_REVIEWS:
            print(f"Reached target of {MAX_REVIEWS} reviews")
            break
        
        # Normal scrolling
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        random_sleep(0.7, 0.3)
        
        if scrolls % 5 == 0:
            random_sleep(2, 1)
            # Add a random small scroll up and down to trigger more loading
            if random.random() > 0.7:  # 30% chance
                scroll_up = random.randint(100, 300)
                current_scroll = driver.execute_script("return arguments[0].scrollTop", scrollable_div)
                driver.execute_script(f"arguments[0].scrollTop = {current_scroll - scroll_up}", scrollable_div)
                random_sleep(0.5, 0.2)
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        updated_reviews = len(driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf, div[jscontroller="e6Mltc"]'))
        
        print(f"Scroll {scrolls+1}: {updated_reviews} reviews loaded")
        
        if updated_reviews == reviews_before:
            no_new_reviews_count += 1
            
            # Try force loading techniques when we haven't seen new reviews for a while
            if no_new_reviews_count % 3 == 0 and no_new_reviews_count < 15:
                technique = random.choice(force_loading_techniques)
                print(f"Trying force loading technique - no new reviews seen for {no_new_reviews_count} scrolls")
                try:
                    technique()
                except Exception as e:
                    print(f"Force loading technique failed: {str(e)}")
            
            # Only stop after significantly more attempts
            if no_new_reviews_count >= 15:
                print("No new reviews after multiple scrolls, stopping")
                break
        else:
            no_new_reviews_count = 0
        
        reviews_before = updated_reviews
        
        if new_height == last_height:
            consecutive_same_height += 1
            
            # Try more aggressive scrolling when height isn't changing
            if consecutive_same_height == 2:
                print("Scroll height unchanged, trying aggressive scrolling...")
                try:
                    # Scroll up and down vigorously
                    current_top = driver.execute_script("return arguments[0].scrollTop", scrollable_div)
                    driver.execute_script(f"arguments[0].scrollTop = {current_top - 500}", scrollable_div)
                    random_sleep(1, 0.5)
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                    random_sleep(1, 0.5)
                except Exception as e:
                    print(f"Aggressive scrolling failed: {str(e)}")
            
            # Only stop after more consecutive same heights
            if consecutive_same_height >= 7:
                print("Can't scroll further, all reviews loaded")
                break
        else:
            consecutive_same_height = 0
        
        last_height = new_height
        scrolls += 1
        
        if scrolls >= 200:
            print("Reached maximum scroll limit")
            break
    
    print("Collecting review data...")
    review_cards = driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf, div[jscontroller="e6Mltc"]')
    print(f"Found {len(review_cards)} reviews")
    
    if len(review_cards) > MAX_REVIEWS:
        review_cards = review_cards[:MAX_REVIEWS]
    
    data = []
    for i, card in enumerate(review_cards):
        try:
            name = extract_text_from_element(card, [".d4r55", ".TSUbDb", "a.WNxzHc", "a[href*='contrib']"])
            rating = extract_rating(card)
            content = extract_text_from_element(card, [".wiI7pd", ".MyEned", ".review-content"])
            
            if content and len(content) < 100:
                try:
                    more_button = find_clickable_element(card, ["button.w8nwRe", "span.review-more-link", "button[aria-label*='Baca selengkapnya']"])
                    if more_button:
                        driver.execute_script("arguments[0].click();", more_button)
                        random_sleep(0.5, 0.2)
                        expanded_content = extract_text_from_element(card, [".wiI7pd", ".MyEned", ".review-content"])
                        if expanded_content and len(expanded_content) > len(content):
                            content = expanded_content
                except:
                    pass
            
            data.append({
                'nama': name,
                'rating': rating,
                'isi_review': content
            })
            
            if (i+1) % 20 == 0:
                print(f"Processed {i+1} reviews")
        except Exception as e:
            print(f"Error extracting review #{i+1}: {str(e)}")
    
    if data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        place_name = "unknown_place"
        try:
            place_title = driver.title
            place_name = re.sub(r'[\\/*?:"<>|]', "", place_title).strip()
            place_name = re.sub(r'\s+', "_", place_name)
        except:
            pass
        
        filename = os.path.join(output_folder, f"gmaps_reviews_{place_name}_{timestamp}.csv")
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"✅ Data successfully saved to: {filename}")
        print(f"Total reviews: {len(data)}")
    else:
        print("❌ No review data collected")
    
    driver.quit()
    
    try:
        if os.path.exists(temp_dir) and "chrome_temp_data" in temp_dir:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception as e:
        print(f"Failed to delete temporary folder: {str(e)}")
    
    print("Process complete!")

def try_click_review_and_back(driver, scrollable_div):
    """Try to click a review and go back to scrolling to trigger more loading"""
    try:
        reviews = driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf, div[jscontroller="e6Mltc"]')
        if reviews:
            # Click a random review
            target_review = random.choice(reviews)
            driver.execute_script("arguments[0].click();", target_review)
            random_sleep(1, 0.5)
            # Go back to scrolling
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
    except Exception as e:
        print(f"Review click attempt failed: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()