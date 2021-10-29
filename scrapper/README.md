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
- Change the value in the variable ***NUMBER_OF_POSTS*** (in *scraper.py*)
- Put the path of ChromeDriver in the variable ***chrome_path*** (in *scraper.py*)
```python
# In this variable you need set the url from which you want to receive data
page_url: str = "https://www.reddit.com/top/?t=month"

# In this variable you need put the path to your chromedriver.exe
chrome_path: str = chrome_path

# In this variable you need to set the number of posts from which data will be collected
NUMBER_OF_POSTS: int = 100
```
Then you need run file ***scraper.py***

Here's the output:
```python
{'unique_id': 'b5234445459b11ecaa4cbc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/MadeMeSmile/comments/qkq3a2/my_kid_was_a_little_sad_after_not_seeing_any/', 'user_name': 'Atillion', 'post_date': '13 days ago', 'number_of_comments': 1300, 'number_of_votes': 176000, 'post_karma': 57633, 'comment_karma': 85399, 'user_karma': 188754, 'user_cake_day': 'October 31, 2015'}
{'unique_id': 'b5a804c0459b11ecba08bc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/MadeMeSmile/comments/qgjrsc/reddit_this_is_my_child_i_apologize_for_nothing/', 'user_name': 'Atillion', 'post_date': '19 days ago', 'number_of_comments': 1900, 'number_of_votes': 170000, 'post_karma': 57633, 'comment_karma': 85399, 'user_karma': 188754, 'user_cake_day': 'October 31, 2015'}
{'unique_id': 'b5f82080459b11ec9f7bbc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/funny/comments/qjqv3x/this_halloween_im_an_antifaxxer_and_theres_no/', 'user_name': 'thatszamora', 'post_date': '14 days ago', 'number_of_comments': 263, 'number_of_votes': 165000, 'post_karma': 19855, 'comment_karma': 49, 'user_karma': 26913, 'user_cake_day': 'April 4, 2019'}
{'unique_id': 'b63d8e00459b11ecaa62bc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/antiwork/comments/q9dwp6/whos_the_boss_now/', 'user_name': 'tylerro2', 'post_date': '1 month ago', 'number_of_comments': 3600, 'number_of_votes': 161000, 'post_karma': 9381, 'comment_karma': 731, 'user_karma': 19103, 'user_cake_day': 'June 15, 2020'}
{'unique_id': 'b6b5a427459b11ecab46bc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/pics/comments/qlkjo5/im_a_rescuer_for_a_raptor_rehab_and_i_got_the/', 'user_name': 'Wildlife-outside', 'post_date': '12 days ago', 'number_of_comments': 4000, 'number_of_votes': 156000, 'post_karma': 12557, 'comment_karma': 33449, 'user_karma': 57113, 'user_cake_day': 'January 17, 2021'}
```
All this data saves in txt file (by this fucntion). If you want to save data in another format, just reformat this function.
```python
from datetime import datetime
def data_to_file(result_list):
    """This function writes the final data to a file."""
    now: str = datetime.now().strftime("%Y%m%d%H%M")
    with open("reddit-" + now + ".txt", "a") as file:
        for i in range(len(result_list)):
            file.write(str(result_list[i]) + "\n")
```
## Issues
Feel free to open an issue if you have any problem using the module.
#### Good luck!