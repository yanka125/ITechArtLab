import logging
import time
from functools import wraps
from uuid import uuid1
from threading import Thread
from queue import Queue
import json

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from config import chrome_path


# Set the url from which you want to receive data
page_url: str = "https://www.reddit.com/top/?t=month"

# Put the path to your chromedriver.exe
chrome_path: str = chrome_path

# Set the number of posts from which data will be collected
NUMBER_OF_POSTS: int = 100

# Make a queue for collecting data
q = Queue()

# Count the number of posted posts
COUNTER: int = 1

# Access the user's url
headers: dict[str:str] = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,image/apng,*/*;q=0.8,application"
              "/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
                  "/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari"
                  "/537.36"
}


def measure(func):
    """Decorator to calculate the amount of time a func takes to execute.

    :param func: function for measuring execution time
    :return: execution time
    """
    @wraps(func)
    def _time_it(*args, **kwargs):
        start: int = int(round(time.time()))
        try:
            return func(*args, **kwargs)
        finally:
            end: int = int(round(time.time())) - start
            print(f"Total execution time: {end if end > 0 else 0} sec")

    return _time_it


def get_logger():
    """Function to configure the logger.

    :return: logger instance
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    return logger


# Initializes the logger
logger = get_logger()


@measure
def main():
    """Function to configure and launche the scrapper."""
    driver = init_driver(chrome_path)
    get_data(driver, page_url)
    driver.quit()


def init_driver(executable_path: str):
    """Function to get the instance of chrome web driver.

    :param executable_path: path to chrome driver
    :type executable_path: str
    :return: driver instance
    :rtype: WebDriver
    """
    service = Service(executable_path)
    options = webdriver.ChromeOptions()
    # This option allows running Chrome in a headless/server environment
    options.add_argument('headless')
    driver = webdriver.Chrome(service=service, options=options)
    '''This option tells Selenium that we would like it to wait for
    a certain amount of time before throwing an exception that if
    it cannot find the element on the page.'''
    driver.implicitly_wait(20)  # seconds
    return driver


def get_data_from_user_url(user_url: str):
    """Collect required data from the user's page.

    :param  user_url: user page url
    :type user_url: str
    :return: parameters with extracted user data
    :rtype: tuple
    """
    response = requests.get(url=user_url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    # Extract block of page with required data in json format and convert it to dictionary
    elem: str = soup.find("script", {"id": "data"}).text.split('=', 1)[1].rstrip(';')
    data: dict = json.loads(elem)['profiles']['about']
    comment_karma = None
    post_karma = None

    # Find required values in dictionary
    for key in data:
        comment_karma = data[key]['karma']['fromComments']
        post_karma = data[key]['karma']['fromPosts']

    # Find required data in html element by id
    user_karma_text: str = soup.find("span", {"id": "profile--id-card--highlight-tooltip--karma"}).text
    user_karma: int = int((user_karma_text.replace(',', '')))
    user_cake_day: str = soup.find("span", {"id": "profile--id-card--highlight-tooltip--cakeday"}).text

    # Checks if all required data is correct
    if post_karma is None or comment_karma is None or user_karma is None or user_cake_day is None:
        pass
    else:
        return post_karma, comment_karma, user_karma, user_cake_day


def get_data_from_posts():
    """Function to check and collect all required data from one post,
    and send post request to api."""
    try:
        # Gets an item from the queue in order to get all the necessary data from this item
        element = q.get()
        # Assign unique_id to post
        unique_id = uuid1().hex

        # Extract post data from html element
        post_date: str = element.find_element(By.CLASS_NAME, "_3jOxDPIQ0KaOWpzvSQo-1s").text
        post_category: str = element.find_element(By.CLASS_NAME, "_2mHuuvyV9doV3zwbZPtIPG").text[2:]

        number_of_votes_text: str = element.find_element(By.CLASS_NAME, "_1E9mcoVn4MYnuBQSVDt1gC").text
        if 'k' in number_of_votes_text:
            number_of_votes: int = int(float(number_of_votes_text.replace('k', '')) * 1000)
        else:
            number_of_votes: int = int(number_of_votes_text)

        number_of_comments_text: str = element.find_element(By.CLASS_NAME, 'FHCV02u6Cp2zYL0fhQPsO').text
        if 'k Comments' in number_of_comments_text:
            number_of_comments = int(float(number_of_comments_text.replace('k Comments', '')) * 1000)
        else:
            number_of_comments = int(number_of_comments_text.replace('Comments', ''))

        post_url: str = element.find_element(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s').get_attribute("href")
        user_url: str = element.find_element(By.CLASS_NAME, '_2tbHP6ZydRpjI44J3syuqC').get_attribute("href")
        user_name: str = user_url[user_url.index('/user/') + 6:len(user_url) - 1]

        # Checks if all required data is correct
        if unique_id is None or post_date is None or number_of_comments is None or post_category is None \
                or number_of_votes is None or post_url is None or user_url is None or user_name == "[deleted]":
            pass
        else:
            (post_karma, comment_karma, user_karma, user_cake_day) = get_data_from_user_url(user_url)

            # When all the data from one post is verified, create a dictionary and make post request
            post = {
                "unique_id": unique_id,
                "post_url": post_url,
                "user_name": user_name,
                "post_date": post_date,
                "number_of_comments": number_of_comments,
                "number_of_votes": number_of_votes,
                "post_karma": post_karma,
                "comment_karma": comment_karma,
                "user_karma": user_karma,
                "user_cake_day": user_cake_day,
            }
            requests.post('http://localhost:8087/posts/', json=post)
            logger.info("All data from post collected successfully")

            # Check how many posts we already sent to api
            global COUNTER
            COUNTER += 1

        # Tells that element from queue is processed and removes it from queue
        q.task_done()
    except Exception as _ex:
        logger.warning(_ex)
        q.task_done()


def get_data(driver, url: str):
    """
    Function to find posts on page url.

    :param driver: driver instance
    :param url: url of the page
    :type url: str
    :type driver: WebDriver
    """
    driver.get(url)
    actions = ActionChains(driver)
    # Start counting posts
    i: int = 1   # always 1

    while COUNTER < NUMBER_OF_POSTS:
        try:
            # Find post on page_url
            element = driver.find_element(By.XPATH, "(//div[@data-testid = 'post-container'])[" + str(i) + "]")
            # Puts the post into the queue for further processing by multiple threads
            q.put(element)
            # Run thread for each element in queue
            Thread(target=get_data_from_posts).start()
            # Move to next element
            actions.move_to_element(element).perform()
            i += 1
        except Exception as _ex:
            logger.error(_ex)

    # Waits until all elements in the queue are processed
    q.join()


if __name__ == "__main__":
    main()
