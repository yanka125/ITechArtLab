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
{'unique_id': '15fce0bb38ae11ec9cccbc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/antiwork/comments/q82vqk/quit_my_job_last_night_it_was_nice_to_be_home_to/', 'user_name': 'hestolemysmile', 'user_karma': '130,613', 'user_cake_day': 'November 5, 2019', 'post_karma': '28225', 'comment_karma': '9319', 'post_date': '15 days ago', 'number_of_comments': '12.6k Comments', 'number_of_votes': '254k', 'post_category': 'antiwork'}
{'unique_id': '1b887edd38ae11ec8b27bc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/memes/comments/q1b13o/reddit_might_be_shit_but_its_our_shit/', 'user_name': '_Floydian', 'user_karma': '202,360', 'user_cake_day': 'April 11, 2018', 'post_karma': '133588', 'comment_karma': '47290', 'post_date': '25 days ago', 'number_of_comments': '1.5k Comments', 'number_of_votes': '196k', 'post_category': 'memes'}
{'unique_id': '1d9cac8838ae11ecb52ebc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/WhitePeopleTwitter/comments/py8nsn/id_like_to_see_it/', 'user_name': 'MessyGuy01', 'user_karma': '253,799', 'user_cake_day': 'March 22, 2019', 'post_karma': '220589', 'comment_karma': '16226', 'post_date': '1 month ago', 'number_of_comments': '5.4k Comments', 'number_of_votes': '170k', 'post_category': 'WhitePeopleTwitter'}
{'unique_id': '1f146be838ae11ec88dbbc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/MadeMeSmile/comments/qgjrsc/reddit_this_is_my_child_i_apologize_for_nothing/', 'user_name': 'Atillion', 'user_karma': '148,548', 'user_cake_day': 'October 31, 2015', 'post_karma': '50463', 'comment_karma': '70505', 'post_date': '2 days ago', 'number_of_comments': '1.8k Comments', 'number_of_votes': '167k', 'post_category': 'MadeMeSmile'}
{'unique_id': '2104cc6238ae11ec9f97bc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/antiwork/comments/q9dwp6/whos_the_boss_now/', 'user_name': 'tylerro2', 'user_karma': '18,937', 'user_cake_day': 'June 15, 2020', 'post_karma': '9380', 'comment_karma': '731', 'post_date': '13 days ago', 'number_of_comments': '3.6k Comments', 'number_of_votes': '155k', 'post_category': 'antiwork'}
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