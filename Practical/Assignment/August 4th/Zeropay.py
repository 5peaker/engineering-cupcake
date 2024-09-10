from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from geopy.geocoders import Nominatim
import pymysql
import pandas as pd
import numpy as np
import platform
from matplotlib import font_manager, rc
import folium, json
from IPython.display import display, HTML
from collections import Counter
# Import necessary modules
import matplotlib.pyplot as plt
# Define helper functions
def extract_address(addr):
    match = re.search(r'(서울특별시 강동구.*?)(?:\s+02|\s+010|\s+070|\s+0|$)', addr)
    if match:
        address = match.group(1).strip()
        address = re.sub(r'\s*\(.*?\)', '', address)
        return address
    return None

def extract_name(addr):
    match = re.search(r'(?:점업|점)\s*(.*?)\s*서울특별시 강동구', addr)
    return match.group(1).strip() if match else None

# Create a class for Selenium scraping
class SeleniumScraper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.addr_s = []
        self.driver = None

    def scrape_page(self, url):
        edge_service = EdgeService(executable_path=self.driver_path)
        edge_options = EdgeOptions()
        self.driver = webdriver.Edge(service=edge_service, options=edge_options)
        self.driver.get(url)
        time.sleep(60)
        
        addresses = self.driver.find_elements(By.CLASS_NAME, 'cmTable')
        for address in addresses:
            self.addr_s.append(address.text)
            addr.append(address.text)
            print(address.text)

    def quit_driver(self):
        self.driver.quit()

# Set the path to the Edge WebDriver executable
driver_path = 'C:/msedgedriver.exe'

# Create an instance of SeleniumScraper
scraper = SeleniumScraper(driver_path)
url_to_scrape = "https://zeropay.or.kr/UI_HP_009_03.act"  
scraper.scrape_page(url_to_scrape)
scraper.quit_driver()

# Get addr_k from formatted_address.txt
addr_k = []
addr_s = []
with open('formatted_address.txt', 'r') as f:
    addr_k = f.readlines()

# Remove unnecessary columns from couponData
couponData = pd.read_excel('CouponUsage.xlsx', header=2)
couponData = couponData.drop(couponData.columns[[1, 2, 3]], axis=1)
couponData = couponData.rename(columns={couponData.columns[1]: '사용처'})
couponData = couponData.drop(columns=['식권'])

# Rename columns in couponData
couponData = couponData.rename(columns={couponData.columns[1]: '사용처'})

# Create tables in MySQL
conn = pymysql.connect(host='localhost', user='root', password='Blame1-Chastise8-Turmoil1-Pointer7', db='zeropay', charset='utf8')
cur = conn.cursor()
cur.execute("USE zeropay")
cur.execute("DROP TABLE IF EXISTS zeropay")
cur.execute("CREATE TABLE zeropay (name VARCHAR(25), address VARCHAR(50), menu VARCHAR(10), gps_location VARCHAR(45))")
cur.execute("DROP TABLE IF EXISTS payUsage")
cur.execute("CREATE TABLE payUsage (사용일시 CHAR(9), 사용처 VARCHAR(15), 업종 VARCHAR(7))")

# Insert data into payUsage table
for i in range(len(couponData)):
    sql = "INSERT INTO payUsage (사용일시, 사용처, 업종) VALUES (%s, %s, %s)"
    cur.execute(sql, (couponData['사용일시'][i], couponData['사용처'][i], couponData['가맹점업종'][i]))

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

# Insert data into zeropay table
for i in range(len(extracted_names)):
    name = extracted_names[i]
    address = extracted_addresses[i]
    menu = service_a[i]
    gps_location = addr_g[i] if addr_g[i] != "Blank" else None
    gps_location_str = str(gps_location) if gps_location is not None else "Blank"

    sql = "INSERT INTO zeropay (name, address, menu, gps_location) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (name, address, menu, gps_location_str))

# Close connection
conn.close()

# Create a map
maps = []
geo_path = 'skorea-provinces-geo.json'
geo_str = json.load(open(geo_path, encoding='utf-8'))
map1 = folium.Map(
    location=[37.5569835, 127.1744769],
    zoom_start=15,
    tiles='OpenStreetMap',
    attr='Jinseong Choi Testing, 20240824',
    scrollWheelZoom=False,
    zoomControl=False
)

# Add markers to the map
folium.Marker([37.55772265, 127.17013912394845], popup='고덕센트럴푸르지오', icon=folium.Icon(color='red')).add_to(map1)

# Display the map
display(map1)
