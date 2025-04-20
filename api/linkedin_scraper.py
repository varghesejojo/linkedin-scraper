from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, os, time

COOKIES_FILE = 'linkedin_cookies.json'

options = ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = Chrome(options=options)

def scroll_page(driver):
    print('Scrolling page...')
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        try:
            show_more_button = driver.find_element(
                By.XPATH,
                "//button[contains(@class, 'scaffold-finite-scroll__load-button')]//span[text()='Show more results']"
            )
            if show_more_button.is_displayed():
                print("Clicking 'Show more results' button...")
                show_more_button.click()
                time.sleep(2)
        except Exception as e:
            # Button not found, which is fine
            pass

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def linkedin_login(username, password):
    print('Logging into LinkedIn...')
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)
    
    # Verify login was successful
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@role='combobox' and @aria-label='Search']"))
        )
    except:
        print("Login failed - could not verify successful login")
        return False
    
    cookies = driver.get_cookies()
    data = {
        'timestamp': time.time(), 
        'cookies': cookies
    }
    with open(COOKIES_FILE, 'w') as f:
        json.dump(data, f)
    return True

def load_cookie_session(username=None, password=None):
    print("Attempting to load cookie session...")
    
    if not os.path.exists(COOKIES_FILE):
        print("No cookie file found. Need to login with credentials.")
        if username and password:
            if linkedin_login(username, password):
                return scrape_connections()
        return False

    with open(COOKIES_FILE, 'r') as f:
        data = json.load(f)
    
    # Check if cookies are older than 1 day
    if time.time() - data['timestamp'] > 86400:  # 1 day
        print("Cookies are older than 1 day, may be expired")
        if username and password:
            print("Attempting fresh login...")
            if linkedin_login(username, password):
                return scrape_connections()
        return False

    # Clear existing cookies first
    driver.get("https://www.linkedin.com")
    driver.delete_all_cookies()
    
    # Add saved cookies
    for cookie in data['cookies']:
        # Remove problematic cookie attributes
        for attr in ['sameSite', 'expiry', 'storeId']:
            if attr in cookie:
                del cookie[attr]
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Couldn't add cookie: {e}")

    driver.refresh()
    time.sleep(3)

    # Verify login was successful
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@role='combobox' and @aria-label='Search']"))
        )
        return scrape_connections()
    except:
        print("Cookie session appears invalid. Need fresh login.")
        if username and password:
            if linkedin_login(username, password):
                return scrape_connections()
        return False

def scrape_connections():
    try:
        driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
        time.sleep(3)
    except Exception as e:
        print(f"Failed to navigate to connections: {e}")
        return False

    scroll_page(driver)

    try:
        cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'mn-connection-card')]"))
        )
    except Exception as e:
        print(f"Failed to find connection cards: {e}")
        return False

    connections_data = []
    seen_names = set()
    count = 0

    for card in cards:
        try:
            name_element = card.find_element(By.XPATH, ".//span[contains(@class, 'mn-connection-card__name')]")
            name = name_element.text.strip()
            
            if name in seen_names:
                continue
            seen_names.add(name)
            
            position = ""
            connected_date = ""
            full_profile_url = ""
            
            try:
                position = card.find_element(By.XPATH, ".//span[contains(@class, 'mn-connection-card__occupation')]").text.strip()
            except Exception as e:
                print(e, 'no position')
                
            try:
                date_element = card.find_element(By.XPATH, ".//time")
                connected_date = date_element.get_attribute("datetime") or date_element.text.strip()
            except Exception as e:
                print(e, 'no date_element')
                
            try:    
                profile_link_element = card.find_element(By.XPATH, ".//a[contains(@class, 'mn-connection-card__link')]")
                profile_href = profile_link_element.get_attribute("href")
                full_profile_url = "https://www.linkedin.com" + profile_href if profile_href.startswith("/") else profile_href
            except Exception as e:
                print(e, 'no profile_link_element')
            
            connections_data.append({
                "name": name,
                "position": position,
                "connected_date": connected_date,
                "profile_link": full_profile_url
            })
            count += 1
            print('count***', count)
            
        except Exception as e:
            print(f"Skipping card due to error: {e}")
            continue

    with open("linkedin_connections.json", "w", encoding='utf-8') as f:
        json.dump(connections_data, f, indent=4, ensure_ascii=False)
    driver.quit()

    print(f"Successfully saved {len(connections_data)} connections")
    return True

