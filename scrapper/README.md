# HTTP-RESTful-API using Web Scraper with Selenium and Beautiful Soup in Python

This project is made for automatic web scraping. He is using HTTP-RESTful-API 
service which in turn provides a simple API for basic file manipulation.
It gets a url and a list of sample data which we want to scrape from some page.
This data can be text, url or any html tag value of that page. 
Now this scrapper can find data only on website https://www.reddit.com/.
The service saves the result to a text file named reddit-YYYYMMDD.txt.
***

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

- I recommend using postman to make an HTTP Method's. 
You can download it from the link. 
```bash
https://www.postman.com/downloads/
```
If you decide to use Postman, I recommend turning all the flags to ***OFF*** in the settings section
<p align="center">
  <img src="https://user-images.githubusercontent.com/70767633/141703628-72cba938-fbb9-4445-8832-c2ea4d8d27d9.png" width="1100" height="500"/>
</p>

***
## How to use HTTP server

The ***api.py*** is simple HTTP server which can host the following api's:

- LIST : Uses GET Method to show all posts from the reddit-YYYYMMDD.txt file.
- CREATE : Uses POST Method to Create a new post for the reddit-YYYYMMDD.txt file.
- UPDATE : Uses PUT Method to update an Existing post of the reddit-YYYYMMDD.txt file.
- DELETE : Uses DELETE Method to delete an Existing post from the reddit-YYYYMMDD.txt file.


- Usage of LIST: GET >> http://localhost:8087/posts/ or http://localhost:8087/posts/unique_id
- Usage of CREATE: POST >> http://localhost:8087/posts/
- Usage of UPDATE: PUT >> http://localhost:8087/posts/unique_id
- Usage of DELETE: DELETE >> http://localhost:8087/posts/unique_id

Just run ***api.py*** to run HTTTP server.
***

## How to use scrapper
You only need to specify the url from which you want to receive data and the number of posts you want to receive:
- Change the value in the variable ***page_url*** (in *scraper.py*)
- Change the value in the variable ***NUMBER_OF_POSTS*** (in *scraper.py*)
- Put the path of ChromeDriver in the variable ***chrome_path*** (in *scraper.py*)
```python
from config import chrome_path

# In this variable you need set the url from which you want to receive data
page_url: str = "https://www.reddit.com/top/?t=month"

# In this variable you need put the path to your chromedriver.exe
chrome_path: str = chrome_path

# In this variable you need to set the number of posts from which data will be collected
NUMBER_OF_POSTS: int = 100
```

Then you need run file ***scraper.py*** (Don't forget to check if api.py is running.)

***scraper.py*** make POST request into our simple HTTP server.
Data storages in reddit-YYYYMMDD.txt in the following format:
```txt
{'unique_id': '15fce0bb38ae11ec9cccbc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/antiwork/comments/q82vqk/quit_my_job_last_night_it_was_nice_to_be_home_to/', 'user_name': 'hestolemysmile', 'user_karma': 130613, 'user_cake_day': 'November 5, 2019', 'post_karma': 28225, 'comment_karma': 9319, 'post_date': '15 days ago', 'number_of_comments': 12600, 'number_of_votes': 254000, 'post_category': 'antiwork'}
{'unique_id': '1b887edd38ae11ec8b27bc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/memes/comments/q1b13o/reddit_might_be_shit_but_its_our_shit/', 'user_name': '_Floydian', 'user_karma': 202360, 'user_cake_day': 'April 11, 2018', 'post_karma': 133588, 'comment_karma': 47290, 'post_date': '25 days ago', 'number_of_comments': 1500, 'number_of_votes': 196000, 'post_category': 'memes'}
{'unique_id': '1d9cac8838ae11ecb52ebc5ff4f0ce51', 'post_url': 'https://www.reddit.com/r/WhitePeopleTwitter/comments/py8nsn/id_like_to_see_it/', 'user_name': 'MessyGuy01', 'user_karma': 253799, 'user_cake_day': 'March 22, 2019', 'post_karma': 220589, 'comment_karma': 16226, 'post_date': '1 month ago', 'number_of_comments': 5400, 'number_of_votes': 170000, 'post_category': 'WhitePeopleTwitter'}
```
***
## Issues
Feel free to open an issue if you have any problem using the module.
### Good luck!
