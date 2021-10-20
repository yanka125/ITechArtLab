import time

from bs4 import BeautifulSoup
from selenium import webdriver

# Web scrapper for infinite scrolling page
driver = webdriver.Chrome(executable_path=r"D:\chromedriver.exe")
driver.get("https://www.reddit.com/top/?t=month")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 2  # My laptop is a bit slow so I use 2 sec
screen_height = driver.execute_script(
    "return window.screen.height;")  # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script(
        "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

# Extract Reddit Data
urls = []
soup = BeautifulSoup(driver.page_source, "html.parser")
i = 0
while i < 10:
    for parent in soup.find_all('div', {"data-testid": "post-container"}):
        print(parent.text)
        i += 1
print(i)
