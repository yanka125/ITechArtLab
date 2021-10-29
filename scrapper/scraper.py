import time
from datetime import datetime
from functools import wraps
from uuid import uuid1

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# In this variable you need set the url from which you want to receive data
page_url: str = "https://www.reddit.com/top/?t=month"

# In this variable you need put the path to your chromedriver.exe
chrome_path: str = "D:\chromedriver.exe"

# In this variable you need to set the number of posts from which data will be collected
number_of_posts: int = 5

# This variable used to access the user's url
headers: dict[str, str] = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,image/apng,*/*;q=0.8,application"
              "/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
                  "/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari"
                  "/537.36"
}


def measure(func):
    """This decorator calculates the amount of time a func takes to execute."""
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time.time()))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time.time())) - start
            print(f"Total execution time: {end_ if end_ > 0 else 0} sec")

    return _time_it


@measure
def main():
    """This function configures and launches the scrapper."""
    driver = init_driver(chrome_path)
    get_data_from_page_url(driver, page_url, number_of_posts)
    driver.quit()


def init_driver(executable_path: str):
    """This function gets the instance of chrome web driver."""
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


def get_data_from_user_url(user_url):
    """This function collects required data from the user's page."""
    response = requests.get(url=user_url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    # This variable takes block of the page in which the required data is located
    elem: str = soup.find("script", {"id": "data"}).text
    # This variable find index of required data in string
    index_carma: int = elem.index('"karma":{"fromAwards')
    # This variable find required data in string
    all_carma: str = elem[index_carma:index_carma + 120]
    post_karma: str = all_carma[all_carma.index('"fromPosts":') + 12:
                                all_carma.index('"total"') - 1]
    comment_karma: str = all_carma[all_carma.index('"fromComments":') + 15:
                                   all_carma.index('"fromPosts"') - 1]
    # Variables user_karma and user_cake_day find by html elements
    user_karma: str = soup.find("span",
        {"id": "profile--id-card--highlight-tooltip--karma"}).text
    user_cake_day: str = soup.find("span",
        {"id": "profile--id-card--highlight-tooltip--cakeday"}).text
    return post_karma, comment_karma, user_karma, user_cake_day


def data_to_file(result_list):
    """This function writes the final data to a file."""
    now: str = datetime.now().strftime("%Y%m%d%H%M")
    with open("reddit-" + now + ".txt", "w") as file:
        for i in range(len(result_list)):
            file.write(str(result_list[i]) + "\n")


def get_data_from_page_url(driver, url: str, posts_count: int):
    """This function collects required data from posts."""
    driver.get(url)
    actions = ActionChains(driver)
    # All data from posts will be placed in this list
    result_list: list[dict[str, str]] = []
    # This variable is used to start counting posts
    i: int = 1  # always 1
    while True:
        try:
            unique_id = uuid1().hex
            element = driver.find_element(By.XPATH,
                "(//div[@data-testid = 'post-container'])[" + str(i) + "]")
            post_date: str = element.find_element(By.XPATH,
                "(//a[@class='_3jOxDPIQ0KaOWpzvSQo-1s'])[" + str(i) + "]").text
            post_category: str = element.find_element(By.XPATH,
                "(//div[@class='_2mHuuvyV9doV3zwbZPtIPG']/a[@class='_3ryJoIoycVkA88fy40qNJc'])[" + str(i) + "]").text[2:]
            number_of_votes: str = element.find_element(By.XPATH,
                "(//div[@class='_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo '])[" + str(i) + "]").text
            number_of_comments: str = element.find_element(By.XPATH,
                "(//span[@class='FHCV02u6Cp2zYL0fhQPsO'])[" + str(i) + "]").text
            post_url: str = element.find_element(By.XPATH,
                "(//a[@class='_3jOxDPIQ0KaOWpzvSQo-1s'])[" + str(i) + "]").get_attribute("href")
            user_url: str = element.find_element(By.XPATH,
                "(//div[@class='_2mHuuvyV9doV3zwbZPtIPG']/a[@style='color: rgb(120, 124, 126);'])[" + str(i) + "]").get_attribute('href')
            user_name: str = user_url[user_url.index('/user/') + 6:len(user_url) - 1]
            '''Checking if all data from posts has been collected,
            else skip this post and go back to the beginning of the loop'''
            if post_date is None or post_category is None or number_of_votes is None \
                    or number_of_comments is None or post_url is None or user_url is None:
                actions.move_to_element(element).perform()
                i += 1
                continue
            '''Checking if all data from user page has been collected,
            else skip this post and go back to the beginning of the loop'''
            try:
                (post_karma, comment_karma, user_karma, user_cake_day) = get_data_from_user_url(user_url)
                if post_karma is None or comment_karma is None or user_karma is None \
                        or user_cake_day is None:
                    actions.move_to_element(element).perform()
                    i += 1
                    continue
            except Exception as _ex:
                actions.move_to_element(element).perform()
                i += 1
                continue
            # When all the data from one post is verified, add them to the result list and move to the next element
            actions.move_to_element(element).perform()
            i += 1
            result_list.append(
                {
                    "unique_id": unique_id,
                    "post_url": post_url,
                    "user_name": user_name,
                    "user_karma": user_karma,
                    "user_cake_day": user_cake_day,
                    "post_karma": post_karma,
                    "comment_karma": comment_karma,
                    "post_date": post_date,
                    "number_of_comments": number_of_comments,
                    "number_of_votes": number_of_votes,
                    "post_category": post_category,
                }
            )
            if len(result_list) == posts_count:
                data_to_file(result_list)
                break
        except Exception as _ex:
            print(_ex)


if __name__ == "__main__":
    main()
