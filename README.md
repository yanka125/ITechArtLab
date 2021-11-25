# HTTP-RESTful-API using Web Scraper with Selenium and Beautiful Soup in Python

This project is made for automatic web scraping. He is using HTTP-RESTful-API 
service which in turn provides a simple API for basic file manipulation.
It gets a url and a list of sample data which we want to scrape from some page.
This data can be text, url or any html tag value of that page. 
Now this scrapper can find data only on website https://www.reddit.com/.
The service saves the result to PostgreSQL database or MongoDB database.
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


1. Usage of LIST: GET >> http://localhost:8087/posts/ or http://localhost:8087/posts/{unique_id}'
+ Request all posts: http://localhost:8087/posts/
+ Request post by unique_id: http://localhost:8087/posts/c268a329486411ecb101bc5ff4f0ce51
2. Usage of CREATE: POST >> http://localhost:8087/posts/
+ Example of request http://localhost:8087/posts/ with the following body
```bash
{
    "unique_id": "c1d34103486411ec8c14bc5ff4f0ce51",
    "post_url": "https://www.reddit.com/r/MadeMeSmile/comments/qkq3a2/my_kid_was_a_little_sad_after_not_seeing_any/",
    "user_name": "Atillion",
    "post_date": "17 days ago",
    "number_of_comments": 1300,
    "number_of_votes": 177000,
    "post_karma": 57665,
    "comment_karma": 88685,
    "user_karma": 192229,
    "user_cake_day": "October 31, 2015"
}
```
3. Usage of UPDATE: PUT >> http://localhost:8087/posts/{unique_id}
+ Example of request: http://localhost:8087/posts/c268a329486411ecb101bc5ff4f0ce51 
with the following body.
```bash
{
    "post_url": "https://www.reddit.com/r/funny/comments/qjqv3x/this_halloween_im_an_antifaxxer_and_theres_no/",
    "post_date": "18 days ago",
    "number_of_comments": 262,
    "number_of_votes": 166000,
    "post_karma": 19855,
    "comment_karma": 49,
    "user_karma": 26981,
    "user_cake_day": "April 4, 2019"
}
```
+ You shouldn't add the "unique_id" and "user_name" fields, otherwise, you will receive a 405 error.
+ You shouldn't add non-existent fields, otherwise, you will receive a 405 error.
4. Usage of DELETE: DELETE >> http://localhost:8087/posts/{unique_id}
+ Example of request: http://localhost:8087/posts/c268a329486411ecb101bc5ff4f0ce51

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
Data is stored in PostgreSQL database:

In __init__ method of __Database__ class, you need to add next data:
+ Name of your database **(db_name)**
+ Name of your user **(db_user)**
+ Password of your database **(db_password)**
+ Your host **(db_host)**
+ Your port **(db_port)**

Example of data:
+ db_name = "Scrapper"
+ db_user = "Postgres"
+ db_password = "qwerty"
+ db_host = "127.0.0.1"
+ db_port = "5432"
```python
class Database(object):

    connection = None
    cursor = None

    def __init__(self):
        if self.connection is None:
            try:
                self.connection = connect(
                     database=db_name,
                     user=db_user,
                     password=db_password,
                     host=db_host,
                     port=db_port,
                )
                self.connection.autocommit = True
                print("Connection to PostgreSQL DB successful")
```
***
## Issues
Feel free to open an issue if you have any problem using the module.
### Good luck!
