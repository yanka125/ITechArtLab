# Web Scraper with Selenium and Beautiful Soup in Python

This project is made for automatic web scraping. It gets a url and a list of sample data which we want to scrape from some page.
This data can be text, url or any html tag value of that page. Now this scrapper can find data only on website "https://www.reddit.com/".


## Installation

It's compatible with python 3.9

- Create you virtual environment (read_documentation)
```bash
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
```

- Install latest version using git:
```bash
$ git clone https://github.com/yanka125/ITechArtLab
```

- Install all packages using pip 
```bash
$ pip install -r requirements.txt
```

- Install latest stable release of ChromeDriver
```bash
https://chromedriver.chromium.org/
```

## How to use

You only need to specify the url from which you want to receive data and the number of posts you want to receive:
- Change the value in the variable ***page_url*** (in *scraper.py*)
- Change the value in the variable ***number_of_posts*** (in *scraper.py*)
- Put the path of ChromeDriver in the variable ***chrome_path*** (in *scraper.py*)
```python
# In this variable you need set the url from which you want to receive data
page_url: str = "https://www.reddit.com/top/?t=month"

# In this variable you need put the path to your chromedriver.exe
chrome_path: str = "D:\chromedriver.exe"

# In this variable you need to set the number of posts from which data will be collected
number_of_posts: int = 5
```
Then you need run file ***scraper.py***

Here's the output:
```python
{"unique_id": "4a9a7f4a457211ec8206bc5ff4f0ce51", "post_url": "https://www.reddit.com/r/MadeMeSmile/comments/qgjrsc/reddit_this_is_my_child_i_apologize_for_nothing/", "user_name": "Atillion", "post_date": "19 days ago", "number_of_comments": 1900, "number_of_votes": 170000, "post_karma": 57632, "comment_karma": 85341, "user_karma": 188695, "user_cake_day": "October 31, 2015"}
{"unique_id": "4b16db3b457211ecb93ebc5ff4f0ce51", "post_url": "https://www.reddit.com/r/antiwork/comments/q9dwp6/whos_the_boss_now/", "user_name": "tylerro2", "post_date": "1 month ago", "number_of_comments": 3600, "number_of_votes": 161000, "post_karma": 9381, "comment_karma": 731, "user_karma": 19103, "user_cake_day": "June 15, 2020"}
{"unique_id": "4b569a81457211ec8ae3bc5ff4f0ce51", "post_url": "https://www.reddit.com/r/pics/comments/qlkjo5/im_a_rescuer_for_a_raptor_rehab_and_i_got_the/", "user_name": "Wildlife-outside", "post_date": "12 days ago", "number_of_comments": 4000, "number_of_votes": 156000, "post_karma": 12557, "comment_karma": 33449, "user_karma": 57113, "user_cake_day": "January 17, 2021"}
{"unique_id": "4ad146b6457211ecbad8bc5ff4f0ce51", "post_url": "https://www.reddit.com/r/funny/comments/qjqv3x/this_halloween_im_an_antifaxxer_and_theres_no/", "user_name": "thatszamora", "post_date": "14 days ago", "number_of_comments": 263, "number_of_votes": 165000, "post_karma": 19855, "comment_karma": 49, "user_karma": 26913, "user_cake_day": "April 4, 2019"}
{"unique_id": "4c4b0b38457211ecb493bc5ff4f0ce51", "post_url": "https://www.reddit.com/r/nextfuckinglevel/comments/qf7u2z/man_just_did_a_vocal_warmup_with_70k_people_in/", "user_name": "_Xyreo_", "post_date": "21 days ago", "number_of_comments": 2800, "number_of_votes": 145000, "post_karma": 829646, "comment_karma": 20817, "user_karma": 1067084, "user_cake_day": "February 28, 2021"}
```
All this data saves in txt file (by this fucntion). If you want to save data in another format, just reformat this function.
```python
from datetime import datetime
def data_to_file(result_list):
    """This function writes the final data to a file."""
    now: str = datetime.now().strftime("%Y%m%d%H%M")
    with open("reddit-" + now + ".txt", "w") as file:
        for i in range(len(result_list)):
            file.write(str(result_list[i]) + "\n")
```
## Issues
Feel free to open an issue if you have any problem using the module.
#### Good luck!