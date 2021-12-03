import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import List, Tuple

import utils
from config import api_host, api_port
from config import mongo_uri, mongo_db_name
from config import db_name, db_user, db_password, db_host, db_port
from utils import convert_posts_to_dict, check_url, concat_posts_to_str

from databases import MongoDB, PostgreSQL


# Create an instances of the classes for the databases actions
mongodb = MongoDB(mongo_uri, mongo_db_name)
postgresql = PostgreSQL(db_name, db_user, db_password, db_host, db_port)


class ServiceHandler(BaseHTTPRequestHandler):
    def _set_headers(self, response_code: int):
        """Function to set common headers and pass different responses codes.

        :param response_code: response code
        """
        self.send_response(response_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def _get_posts(self, unique_id: str = None):
        """Function to get data from database.

        :param unique_id: unique post ID
        :return: all data from database
        :rtype: List[Tuple]
        """
        return mongodb.get_from_database(unique_id)

    def do_GET(self):
        """Function to receive get request. Valid request url path:
        /posts/ or /posts/{unique_id}."""
        (is_valid_url, unique_id) = check_url(self.path, "^/posts/([a-z0-9]+)?/?$", True)

        if is_valid_url:
            # If requested all posts
            if unique_id is None:
                posts = convert_posts_to_dict(self._get_posts())
                posts_str = concat_posts_to_str(posts)
                self._set_headers(200)
                # Write all posts in json format in response body
                self.wfile.write(posts_str.encode("utf-8"))
            # If one post is requested by unique_id
            else:
                post = convert_posts_to_dict(self._get_posts(unique_id))
                if post:
                    self._set_headers(200)
                    # Write one post in json format in response body
                    self.wfile.write(str(json.dumps(post[0])).encode("utf-8"))
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
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            post_json = json.loads(post_data)
            post_id = post_json[utils.POST_PK]
            posts = convert_posts_to_dict(self._get_posts(post_id))

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
                mongodb.write_to_database(data_to_posts, data_to_users)
                postgresql.write_to_database(data_to_posts, data_to_users)
                self._set_headers(201)

        # If invalid url path
        else:
            self._set_headers(400)

    def do_PUT(self):
        """Function to receive put request. Valid request url path:
        /posts/{unique_id}."""
        (is_valid_url, unique_id) = check_url(self.path, "^/posts/([a-z0-9]+)/?$", True)

        if is_valid_url:
            post = convert_posts_to_dict(self._get_posts(unique_id))

            if post:
                # Reading the request body
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length).decode("utf-8")
                post_json = json.loads(post_data)
                # Take post data
                elem = post[0]
                if utils.POST_PK in post_json:
                    self._set_headers(405)
                else:
                    # Check if valid keys are passed and update database column
                    if all(key in elem for key in post_json):
                        elem.update(post_json)
                        mongodb.update_database(elem, unique_id)
                        postgresql.update_database(elem, unique_id)
                        self._set_headers(200)
                    else:
                        self._set_headers(405)
            # If requested post doesn't exists in database
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
            posts = convert_posts_to_dict(self._get_posts())
            elem = next((post for post in posts if post[utils.POST_PK] == unique_id), None)

            # If requested post exists in database
            if elem:
                mongodb.delete_from_database(unique_id)
                postgresql.delete_from_database(unique_id)
                self._set_headers(200)
            else:
                self._set_headers(404)

        # If invalid url path
        else:
            self._set_headers(400)


# Server Initialization
server = HTTPServer((api_host, api_port), ServiceHandler)
server.serve_forever()
