import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

from PostgreSQL import Database
from config import api_host, api_port


# Create an instance of the class for the database actions
dbs = Database()


def get_posts(unique_id=None):
    """Read all post data from database and return list of dictionaries.

    :param unique_id: unique post id
    :type unique_id: str
    :return: all post data
    :rtype: list[dict]
    """
    database_data: list[tuple] = dbs.get_from_database(unique_id)
    result_list: list[dict] = []
    for post in database_data:
        # Add all post data to list
        result_list.append(
            {
                "unique_id": post[0],
                "post_url": post[1],
                "user_name": post[2],
                "post_date": post[3],
                "number_of_comments": post[4],
                "number_of_votes": post[5],
                "post_karma": post[6],
                "comment_karma": post[7],
                "user_karma": post[8],
                "user_cake_day": post[9]
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
        """Function to set common headers and pass different responses codes.

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
            # If requested all posts
            if unique_id is None:
                posts = get_posts()
                posts_str = convert_posts_in_str(posts)
                self._set_headers(200)
                # Write all posts in json format in response body
                self.wfile.write(posts_str.encode('utf-8'))
            # If one post is requested by unique_id
            else:
                post = get_posts(unique_id)
                if post:
                    self._set_headers(200)
                    # Write one post in json format in response body
                    self.wfile.write(str(json.dumps(post[0])).encode('utf-8'))
                else:
                    self._set_headers(404)
        # If invalid url path
        else:
            self._set_headers(400)

    def do_POST(self):
        """Function to receive post request and writes new post into database.
        Valid request url path: /posts/."""
        (is_valid_url, unique_id) = check_url(self.path, "^/posts/$", False)

        if is_valid_url:
            # Reading the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_json = json.loads(post_data)
            posts = get_posts(post_json['unique_id'])
            # If post with this unique_id already exists
            if posts:
                self._set_headers(405)
            else:
                data_to_users = (
                    post_json["user_name"],
                    post_json["post_karma"],
                    post_json["comment_karma"],
                    post_json["user_karma"],
                    post_json["user_cake_day"],
                )
                data_to_posts = (
                    post_json["unique_id"],
                    post_json["post_url"],
                    post_json["user_name"],
                    post_json["post_date"],
                    post_json["number_of_comments"],
                    post_json["number_of_votes"],
                )
                dbs.send_to_database(data_to_posts, data_to_users)
                self._set_headers(201)

        # If invalid url path
        else:
            self._set_headers(400)

    def do_PUT(self):
        """Function to receive put request. Valid request url path:
        /posts/{unique_id}."""
        (is_valid_url, unique_id) = check_url(self.path, "^/posts/([a-z0-9]+)/?$", True)

        if is_valid_url:
            post = get_posts(unique_id)

            if post:
                # Reading the request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                post_json = json.loads(post_data)
                # Take post data
                elem = post[0]
                if "unique_id" in post_json:
                    self._set_headers(405)
                else:
                    # Check if valid keys are passed and update database column
                    if all(key in elem for key in post_json):
                        elem.update(post_json)
                        data_to_users = (
                            elem["post_karma"],
                            elem["comment_karma"],
                            elem["user_karma"],
                            elem["user_cake_day"],
                        )
                        data_to_posts = (
                            elem["post_url"],
                            elem["post_date"],
                            elem["number_of_comments"],
                            elem["number_of_votes"],
                        )
                        user_name = elem["user_name"]
                        dbs.update_database(data_to_users, user_name, data_to_posts, unique_id)
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

            # If requested post exists in database
            if elem is not None:
                dbs.delete_from_database(unique_id)
                self._set_headers(200)
            else:
                self._set_headers(404)

        # If invalid url path
        else:
            self._set_headers(400)


# Server Initialization
server = HTTPServer((api_host, api_port), ServiceHandler)
server.serve_forever()
