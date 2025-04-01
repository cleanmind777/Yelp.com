from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, re
from urllib.parse import urlparse, parse_qs, unquote, urlunparse
import json
import csv
driver = webdriver.Chrome()
# Open a webpage
driver.get("https://www.yelp.com/search?find_desc=Dentist&find_loc=California+City%2C+CA%2C+United+States")

# Scroll until no more content is loaded
wait = WebDriverWait(driver, 100)
time.sleep(10)