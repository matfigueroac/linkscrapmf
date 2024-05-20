from flask import Flask, request, render_template, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import pandas as pd
import time
import random
import os

app = Flask(__name__)

# Path to your ChromeDriver
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'  # Update this to the actual path

def simulate_human_behavior(driver):
    for _ in range(random.randint(5, 10)):
        random_x = random.randint(0, driver.execute_script("return window.innerWidth"))
        random_y = random.randint(0, driver.execute_script("return window.innerHeight"))
        driver.execute_script(f"window.scrollTo({random_x}, {random_y});")
        time.sleep(random.uniform(0.1, 0.5))
    for _ in range(random.randint(3, 6)):
        driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")
        time.sleep(random.uniform(0.2, 0.7))

def get_profile_info(url, driver):
    driver.get(url)
    time.sleep(random.uniform(5, 10))
    simulate_human_behavior(driver)
    profile_info = {}

    try:
        full_name_element = driver.find_element(By.CSS_SELECTOR, 'h1.text-heading-xlarge')
        headline_element = driver.find_element(By.CSS_SELECTOR, 'div.text-body-medium.break-words')
        location_element = driver.find_element(By.CSS_SELECTOR, 'span.text-body-small.inline.t-black--light.break-words')

        full_name = full_name_element.text.strip() if full_name_element else 'not available'
        headline = headline_element.text.strip() if headline_element else 'not available'
        location = location_element.text.strip() if location_element else 'not available'

        if full_name != 'not available':
            name_parts = full_name.split()
            first_name = name_parts[0]
            last_name = name_parts[-1] if len(name_parts) > 1 else 'not available'
        else:
            first_name = last_name = 'not available'

        job_title = company_name = school_name = about = 'not available'

        try:
            job_title_element = driver.find_element(By.CSS_SELECTOR, "SECTION[data-view-name='profile-card']:nth-of-type(7) > DIV:last-of-type > UL:first-of-type > LI:first-of-type > DIV[data-view-name='profile-component-entity']:first-of-type > DIV:last-of-type > DIV:first-of-type > DIV:first-of-type > DIV:first-of-type > DIV:first-of-type > DIV:first-of-type > DIV:first-of-type > SPAN:first-of-type")
            job_title = job_title_element.text.strip() if job_title_element else "not available"
        except Exception as e:
            print(f"Error fetching job title for {url}: {e}")

        try:
            company_name_element = driver.find_element(By.CSS_SELECTOR, 'main [aria-label^="Current company"]')
            company_name = company_name_element.text.strip() if company_name_element else "not available"
        except Exception as e:
            print(f"Error fetching company name for {url}: {e}")

        try:
            school_name = driver.find_element(By.CSS_SELECTOR, '#education + div + div li div span').text.strip()
        except Exception as e:
            print(f"Error fetching school name for {url}: {e}")

        try:
            about = driver.find_element(By.CSS_SELECTOR, '#about + div + div span').text.strip()
        except Exception as e:
            print(f"Error fetching about for {url}: {e}")

        try:
            image_element = driver.find_element(By.CSS_SELECTOR, ".pv-top-card-profile-picture__image--show")
            image_url = image_element.get_attribute('src')
        except Exception as e:
            print(f"Error fetching image URL for {url}: {e}")

        profile_info = {
            'Full Name': full_name,
            'First Name': first_name,
            'Last Name': last_name,
            'Job Title': job_title,
            'Company Name': company_name,
            'School Name': school_name,
            'Location': location,
            'URL': url,
            'About': about,
            'Image': image_url,
            'Headline': headline
        }

    except Exception as e:
        print(f"An error occurred while fetching profile info for {url}: {e}")

    return profile_info

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    linkedin_username = request.form['username']
    linkedin_password = request.form['password']
    urls = request.form['urls'].splitlines()
    file = request.files['file']

    if file:
        urls += file.read().decode('utf-8').splitlines()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

    # Use selenium-stealth to evade bot detection
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    linkedin_login_url = 'https://www.linkedin.com/login'
    driver.get(linkedin_login_url)
    time.sleep(3)

    username = driver.find_element(By.ID, 'username')
    password = driver.find_element(By.ID, 'password')
    username.send_keys(linkedin_username)
    password.send_keys(linkedin_password)
    password.send_keys(Keys.RETURN)
    time.sleep(5)

    data = []
    for url in urls:
        info = get_profile_info(url, driver)
        if info:
            data.append(info)
        time.sleep(random.uniform(5, 10))

    driver.quit()

    df = pd.DataFrame(data, columns=['Full Name', 'First Name', 'Last Name', 'Job Title', 'Company Name', 'School Name', 'Location', 'URL', 'About', 'Image', 'Headline'])
    csv_file = 'LinkedIn_Contacts_Info.csv'
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')

    return send_file(csv_file, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
