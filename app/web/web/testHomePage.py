from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Create a new instance of the ChromeDriver
WebDriver driver = new ChromeDriver()

# go to the home page
driver.get("http://localhost:8000")

print driver.title

driver.get("http://localhost:8000/group/?id=1")
Study = driver.find_element_by_name("Study")

print driver.find_element_by_name("Study")

driver.get("http://localhost:8000/group/?id=2")
print driver.find_element_by_name("Projects")

driver.get("http://localhost:8000/group/?id=3")
print driver.find_element_by_name("zumba")

driver.get("http://localhost:8000/group/?id=4")
print driver.find_element_by_name("time-telling")

driver.get("http://localhost:8000/group/?id=5")
print driver.find_element_by_name("Mobile")

driver.get("http://localhost:8000/group/?id=6")
print driver.find_element_by_name("History")

driver.get("http://localhost:8000/group/?id=7")
print driver.find_element_by_name("CS2150")

driver.get("http://localhost:8000/group/?id=8")
print driver.find_element_by_name("Algorithms")
