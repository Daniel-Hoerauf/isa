from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Create a new instance of the ChromeDriver
WebDriver driver = new ChromeDriver()

# go to the google home page
driver.get("http://localhost:8000/search/")

print driver.title

print driver.find_element_by_name("Search")
