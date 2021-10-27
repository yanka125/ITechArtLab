from functools import wraps
import time
from pprint import pprint
from uuid import uuid1
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

url = "https://www.reddit.com/top/?t=month"
now = datetime.now().strftime("%Y%m%d%H%M")


def measure(func):
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
def scrapper():
    s = Service("D:\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=s, options=options)
    driver.implicitly_wait(20)
    driver.get(url)

    result_list = []
    i = 1

    while True:
        try:
            actions = ActionChains(driver)
            unique_id = uuid1().hex
            element = driver.find_element(By.XPATH,
                                          "(//div[@data-testid = 'post-container'])[" + str(
                                              i) + "]")
            post_date = element.find_element(By.XPATH,
                                             "(//a[@class='_3jOxDPIQ0KaOWpzvSQo-1s'])[" + str(
                                                 i) + "]").text
            # date = element.find_element(By.XPATH,
            #                                  "(//a[@class='_3jOxDPIQ0KaOWpzvSQo-1s'])[" + str(
            #                                      i) + "]")
            # post_date = ''
            # while post_date == '':
            #     actions.move_to_element(date).perform()
            #     time.sleep(2)
            #     post_date = element.find_element(By.XPATH,
            #                                  "(//div[@class='_2J_zB4R1FH2EjGMkQjedwc u6HtAZu8_LKL721-EnKuR'])").text
            post_category = element.find_element(By.XPATH,
                                                 "(//div[@class='_2mHuuvyV9doV3zwbZPtIPG']/a[@class='_3ryJoIoycVkA88fy40qNJc'])[" + str(
                                                     i) + "]").text[2:]
            if post_category == None:
                actions.move_to_element(element).perform()
                i += 1
                continue
            number_of_votes = element.find_element(By.XPATH,
                                                   "(//div[@class='_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo '])[" + str(
                                                       i) + "]").text
            if number_of_votes == None:
                actions.move_to_element(element).perform()
                i += 1
                continue
            number_of_comments = element.find_element(By.XPATH,
                                                      "(//span[@class='FHCV02u6Cp2zYL0fhQPsO'])[" + str(
                                                          i) + "]").text
            if number_of_comments == None:
                actions.move_to_element(element).perform()
                i += 1
                continue
            post_url = element.find_element(By.XPATH,
                                            "(//a[@class='_3jOxDPIQ0KaOWpzvSQo-1s'])[" + str(
                                                i) + "]").get_attribute("href")
            if post_url == None:
                actions.move_to_element(element).perform()
                i += 1
                continue
            user_url = element.find_element(By.XPATH,
                                            "(//div[@class='_2mHuuvyV9doV3zwbZPtIPG']/a[@style='color: rgb(120, 124, 126);'])[" + str(
                                                i) + "]").get_attribute('href')
            user_name = user_url[user_url.index('/user/') + 6:len(user_url) - 1]
            if user_name == None:
                actions.move_to_element(element).perform()
                i += 1
                continue
            response = requests.get(url=user_url, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")
            try:
                elem = soup.find("script", {"id": "data"}).text
                index_carma = elem.index('"karma":{"fromAwards')
                all_carma = elem[index_carma:index_carma + 120]
            except Exception as _ex:
                print(_ex)
            try:
                post_karma = all_carma[
                             all_carma.index('"fromPosts":') + 12:all_carma.index('"total"') - 1]
            except Exception as _ex:
                actions.move_to_element(element).perform()
                i += 1
                continue
            try:
                comment_karma = all_carma[all_carma.index('"fromComments":') + 15:all_carma.index(
                    '"fromPosts"') - 1]
            except Exception as _ex:
                actions.move_to_element(element).perform()
                i += 1
                continue
            try:
                user_karma = soup.find("span", {
                    "id": "profile--id-card--highlight-tooltip--karma"}).text
            except Exception as _ex:
                actions.move_to_element(element).perform()
                i += 1
                continue
            try:
                user_cake_day = soup.find("span", {
                    "id": "profile--id-card--highlight-tooltip--cakeday"}).text
            except Exception as _ex:
                actions.move_to_element(element).perform()
                i += 1
                continue

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

            if len(result_list) == 100:
                # pprint(result_list)
                with open("reddit-" + now + ".txt", 'w') as file:
                    for i in range(len(result_list)):
                        file.write(str(result_list[i]) + '\n')
                break
        except Exception as e:
            print(e)
            break


scrapper()
