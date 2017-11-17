from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Create a new instance of the ChromeDriver
WebDriver driver = new ChromeDriver()

# go to the sign up page
driver.get("http://localhost:8000/signup/")

print driver.title
