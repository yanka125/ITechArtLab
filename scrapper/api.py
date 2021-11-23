import json
import re
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

from PostgreSQL import post_method, get_method, delete_method


def get_posts():
    """
    Read all post data from database and return list of dictionaries.

    :return: all post data
    :rtype: list[dict]
    """
    data = get_method()
    result_list = []
    for t in data:
        result_list.append(
            {
                "unique_id": t[0],
                "post_url": t[1],
                "user_name": t[2],
                "post_date": t[3],
                "number_of_comments": t[4],
                "number_of_votes": t[5],
                "post_karma": t[6],
                "comment_karma": t[7],
                "user_karma": t[8],
                "user_cake_day": t[9]
            }
        )
    return result_list


def check_url(path: str, pattern: str, extract_id: bool):
    """Function to check validity of url path by given regex pattern
    and extract unique_id if it exists in request.

    :param path: resource path from url
    :type path: str
    :param pattern: regex pattern
    :type pattren: str
    :param extract_id: flag to check if unique_id should be extracted
    :type extract_id: bool
    :return: (flag to identify if url is valid, extracted unique id)
    :rtype: tuple
    """
    url = re.search(pattern, path)
    unique_id = None
    is_valid_url = False
    if url is not None:
        is_valid_url = True
        if extract_id:
            unique_id = url.group(1)
    return is_valid_url, unique_id


def convert_posts_in_str(posts: list):
    """Function to convert list of dictionaries with post data
    to list of json strings.

    :param posts: post data
    :type posts: list[dict]
    :return: post data concatenated in string
    :rtype: str
    """
    result_list = []
    for post in posts:
        result_list.append(json.dumps(post))
    result = '\n'.join(result_list)
    return result


class ServiceHandler(BaseHTTPRequestHandler):

    def _set_headers(self, response_code: int):
        """This function sets common headers and passed different responses codes.

        :param response_code: response code
        :type response_code: int
        """
        self.send_response(response_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """Function to receive get request. Valid request url path:
        /posts/ or /posts/{unique_id}."""
        (is_valid_url, unique_id) = check_url(self.path, "^/posts/([a-z0-9]+)?/?$", True)

        if is_valid_url:
            posts = get_posts()

            # If requested all posts
            if unique_id is None:
                posts_str = convert_posts_in_str(posts)
                self._set_headers(200)
                # Write all posts in json format in response body
                self.wfile.write(posts_str.encode('utf-8'))
            # If one post is requested by unique_id
            else:
                elem = next((post for post in posts if post["unique_id"] == unique_id), None)
                if elem is not None:
                    self._set_headers(200)
                    # Write one post in json format in response body
                    self.wfile.write(str(json.dumps(elem)).encode('utf-8'))
                else:
                    self._set_headers(404)
        # If invalid url path
        else:
            self._set_headers(400)

    def do_POST(self):
        """Function to receive post request and writes new post into database.
        Valid request url path: /posts/."""
        (is_valid_url, unique_id) = check_url(self.path,"^/posts/$", False)

        if is_valid_url:
            posts = get_posts()

            # Reading the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_json = json.loads(post_data)
            if post_json['unique_id'] in (post["unique_id"] for post in posts):
                self._set_headers(405)
            else:
                data_to_users = (post_json["user_name"], post_json["post_karma"], post_json["comment_karma"], post_json["user_karma"], post_json["user_cake_day"],)
                data_to_posts = (post_json["unique_id"], post_json["post_url"], post_json["user_name"], post_json["post_date"], post_json["number_of_comments"], post_json["number_of_comments"],)
                post_method(data_to_posts, data_to_users)
                self._set_headers(201)

        # If invalid url path
        else:
            self._set_headers(400)

    def do_PUT(self):
        """Function to receive put request. Valid request url path:
        /posts/{unique_id}."""
        (is_valid_url, unique_id) = check_url(self.path,"^/posts/([a-z0-9]+)/?$", True)

        if is_valid_url:
            posts = get_posts()
            elem = next((post for post in posts if post["unique_id"] == unique_id), None)

            # If requested post exists in file
            if elem is not None:
                # Reading the request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                post_json = json.loads(post_data)

                if "unique_id" in post_json:
                    self._set_headers(405)
                else:
                    # Check if valid keys are passed and overwrite file with updated data
                    if all(key in elem for key in post_json):
                        elem.update(post_json)
                        self._set_headers(200)
                    else:
                        self._set_headers(405)
            # If requested post doesn't exists in file
            else:
                self._set_headers(404)
        # If invalid url path
        else:
            self._set_headers(400)

    def do_DELETE(self):
        """Function to receive delete request. Valid request url path:
        /posts/{unique_id}."""
        (is_valid_url, unique_id) = check_url(self.path, "^/posts/([a-z0-9]+)/?$", True)

        if is_valid_url:
            posts = get_posts()
            elem = next((post for post in posts if post["unique_id"] == unique_id), None)

            # If requested post exists in file
            if elem is not None:
                delete_method(unique_id)
                self._set_headers(200)
            else:
                self._set_headers(404)

        # If invalid url path
        else:
            self._set_headers(400)


# Server Initialization
server = HTTPServer(('localhost', 8087), ServiceHandler)
server.serve_forever()
