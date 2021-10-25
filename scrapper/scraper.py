from pprint import pprint
from uuid import uuid1
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

url = "https://www.reddit.com/top/?t=month"
now = datetime.now().strftime("%Y%m%d%H%M")


def scrapper():
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get(url)
    result_list = []
    i = 1

    while True:
        try:
            unique_id = uuid1().hex
            element = driver.find_element(By.XPATH,
                                          "(//div[@data-testid = 'post-container'])[" + str(
                                              i) + "]")
            # actions = ActionChains(driver)
            # date = element.find_element(By.XPATH,
            #                                 "(//a[@class='_3jOxDPIQ0KaOWpzvSQo-1s'])[" + str(
            #                                     i) + "]")
            # actions.move_to_element(date).perform()
            # post_date = date.find_element(By.XPATH,
            #                                        "(//div[@style='position: absolute; inset: auto auto 0px 0px; transform: translate(296px, -535px);'])").text
            post_category = element.find_element(By.XPATH,
                                                 "(//div[@class='_2mHuuvyV9doV3zwbZPtIPG']/a[@class='_3ryJoIoycVkA88fy40qNJc'])[" + str(
                                                     i) + "]").text[2:]
            number_of_votes = element.find_element(By.XPATH,
                                                   "(//div[@class='_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo '])[" + str(
                                                       i) + "]").text
            number_of_comments = element.find_element(By.XPATH,
                                                      "(//span[@class='FHCV02u6Cp2zYL0fhQPsO'])[" + str(
                                                          i) + "]").text
            post_url = element.find_element(By.XPATH,
                                            "(//a[@class='_3jOxDPIQ0KaOWpzvSQo-1s'])[" + str(
                                                i) + "]").get_attribute("href")
            user_url = element.find_element(By.XPATH,
                                            "(//div[@class='_2mHuuvyV9doV3zwbZPtIPG']/a[@style='color: rgb(120, 124, 126);'])[" + str(
                                                i) + "]").get_attribute('href')
            user_name = user_url[user_url.index('/user/') + 6:len(user_url) - 1]

            response = requests.get(url=user_url, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")
            elem = soup.find("script", {"id": "data"}).text
            index_carma = elem.index('"karma":{"fromAwards')
            all_carma = elem[index_carma:index_carma + 120]
            try:
                post_karma = all_carma[
                             all_carma.index('"fromPosts":') + 12:all_carma.index('"total"') - 1]
            except Exception as _ex:
                post_karma = None
            try:
                comment_karma = all_carma[all_carma.index('"fromComments":') + 15:all_carma.index(
                    '"fromPosts"') - 1]
            except Exception as _ex:
                comment_karma = None
            try:
                user_karma = soup.find("span", {
                    "id": "profile--id-card--highlight-tooltip--karma"}).text
            except Exception as _ex:
                user_karma = None
            try:
                user_cake_day = soup.find("span", {
                    "id": "profile--id-card--highlight-tooltip--cakeday"}).text
            except Exception as _ex:
                user_cake_day = None

            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            i += 1
            # if unique_id or post_url or user_name or number_of_comments or number_of_votes \
            #         or post_category or user_carma or user_cake_day == 'None':
            #     continue

            result_list.append(
                {
                    "unique_id": unique_id,
                    "post_url": post_url,
                    "user_name": user_name,
                    "user_karma": user_karma,
                    "user_cake_day": user_cake_day,
                    "post_karma": post_karma,
                    "comment_karma": comment_karma,
                    # "post_date": post_date,
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
