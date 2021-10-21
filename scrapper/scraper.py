import time
from datetime import datetime
from uuid import uuid1

from bs4 import BeautifulSoup
from selenium import webdriver

now = datetime.now().strftime("%Y%m%d%H%M")

# Web scrapper for infinite scrolling page
driver = webdriver.Chrome(executable_path=r"D:\chromedriver.exe")
driver.maximize_window()
driver.get("https://www.reddit.com/top/?t=month")
time.sleep(3)  # Allow 3 seconds for the web page to open
scroll_pause_time = 2  # Time between scrolling
screen_height = driver.execute_script(
    "return window.screen.height;")  # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script(
        "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height after scrolled, as the scroll height can change after scrolling the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    # if (screen_height) * i > scroll_height:
    #     break
    if i > 100:
        break

# Extract Reddit Data
urls = []
unique_ids = []
dates = []
user_names = []
post_categories = []
numbers_of_comments = []
numbers_of_vote = []
soup = BeautifulSoup(driver.page_source, "html.parser")
for url in soup.find_all("a", class_="_3jOxDPIQ0KaOWpzvSQo-1s"):
    urls.append(url.get("href"))  # Append post url to list
    if len(urls) > 100:
        break
for i in range(len(urls)):
    unique_id = uuid1().hex
    unique_ids.append(unique_id)

for item in soup.find_all('div', class_="_3AStxql1mQsrZuUIFP9xSg nU4Je7n-eSXStTBAPMYt8"):
    data = item.text
    dates.append(data[:7])  # Append post date to list, need to refactor! [data.index('days') - 2:]
    user_names.append(data[
                      :7])  # Append username to list, need to refactor! data.index('u/') + 2:data.index('days') - 2
    post_categories.append(
        data[data.index('r/') + 2:data.index('•')])  # Append post category to list
    if len(dates) > 100 or len(user_names) > 100 or len(post_categories) > 100:
        break

for number in soup.find_all('span', class_="FHCV02u6Cp2zYL0fhQPsO"):
    numbers_of_comments.append(number.text)
    if len(numbers_of_comments) > 100:
        break

for number in soup.find_all('div', class_="_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo"):
    numbers_of_vote.append(number.text)
    if len(numbers_of_vote) > 100:
        break

for i in range(len(urls)):
    str = urls[i] + ';' + unique_ids[i] + ';' + dates[i] + ';' + post_categories[i] + ';' + \
          numbers_of_comments[i] + ';' + numbers_of_vote[i] + ';' + '\n'

    with open("reddit-" + now + ".txt", 'a') as file:
        file.write(str)
