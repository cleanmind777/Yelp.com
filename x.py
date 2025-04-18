import os
import time
import psutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def kill_chrome_processes():
    """Force kill all Chrome processes"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in ('chrome.exe', 'chromedriver.exe'):
            try:
                proc.kill()
            except psutil.NoSuchProcess:
                pass
    time.sleep(2)  # Wait for processes to terminate

def main():
    # Kill existing Chrome processes
    # kill_chrome_processes()
    
    # Configure Chrome options
    options = uc.ChromeOptions()
    
    # Set paths
    user_data_dir = r"C:\Users\cleanmind\AppData\Local\Google\Chrome\User Data\Profile 2"
    chromedriver_path = r"E:\code_example\chromedriver-win64\chromedriver.exe"
    
    # Verify paths exist
    if not os.path.exists(user_data_dir):
        raise FileNotFoundError(f"Chrome profile not found at: {user_data_dir}")
    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"ChromeDriver not found at: {chromedriver_path}")

    # Configure options
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--remote-debugging-port=9222")  # Fixed port for stability
    options.add_argument("--no-first-run")
    options.add_argument("--no-service-autorun")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-default-apps")

    try:
        print("Initializing ChromeDriver...")
        driver = uc.Chrome(
            options=options,
            version_main=135,  # Must match your Chrome version
            driver_executable_path=chromedriver_path,
            service_args=['--verbose'],  # Enable logging
            service_log_path='chromedriver.log'  # Save logs to file
        )
        print("ChromeDriver initialized successfully")

        # Open target website with retry logic
        target_url = "https://www.yelp.com/search?find_desc=Dentist&find_loc=California+City%2C+CA%2C+United+States"
        
        # while True:
        #     next_btn = driver.find_element(By.CSS_SELECTOR, ".pagination-button__09f24__kbFYf.y-css-16wjqqa")
        #     disable = next_btn.get_attribute("disabled")
        #     print(disable)
        #     break
        # Verification steps
        dentists = driver.find_elements(By.CLASS_NAME, " y-css-pwt8yl")
        for dentist in dentists:
            dentist_information = {}
            title_element = dentist.find_element(By.TAG_NAME, "h3")
            dentist_information['title'] = title_element.text
            title_element.click()
            review = driver.find_element(By.CSS_SELECTOR, '[data-testid="BizHeaderReviewCount"]')
            review_rate = review.find_elements(By.TAG_NAME, 'span')[0].text
            review_count = review.find_elements(By.TAG_NAME, 'span')[1].text
            dentist_information['review'] = {
                'rate' : review_rate,
                'count' : review_count
            }
            contact_information = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cookbook-island"]')[0].find_elements(By.CLASS_NAME, 'y-css-4cg16w')
            website = contact_information[0].find_element(By.TAG_NAME, 'a').text
            phone_number = contact_information[1].find_element(By.CLASS_NAME, ' y-css-qn4gww').text
            address = contact_information[2].find_element(By.CLASS_NAME, ' y-css-p0gpmm').text
            dentist_information['contact'] = {
                'website' : website,
                'phone number' : phone_number,
                'address' : address
            }
        driver.save_screenshot("yelp_loaded.png")
        print("Screenshot saved")
        
        # Keep browser open for debugging
        print("Browser will remain open for 300 seconds...")
        time.sleep(300)
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        if os.path.exists('chromedriver.log'):
            with open('chromedriver.log', 'r') as f:
                print("\nChromeDriver Logs:\n", f.read())
    finally:
        if 'driver' in locals():
            driver.quit()
        kill_chrome_processes()

if __name__ == "__main__":
    main()