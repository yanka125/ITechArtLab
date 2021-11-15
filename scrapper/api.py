import json
import re
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import os


def get_posts():
    now: str = datetime.now().strftime("%Y%m%d")
    with open("reddit-" + now + ".txt") as data_file:
        lines = data_file.readlines()
        data = []
        for i in lines:
            data.append(json.loads(i))
        return data


def check_url(path, pattern: str, extract_id: bool):
    url = re.search(pattern, path)
    unique_id = None
    is_valid_url = False
    if url is not None:
        is_valid_url = True
        if extract_id:
            unique_id = url.group(1)
    return is_valid_url, unique_id


def overwrite_file(posts: list):
    now: str = datetime.now().strftime("%Y%m%d")
    result = convert_posts_in_str(posts)
    with open("reddit-" + now + ".txt", "w") as file:
        file.write(result)


def convert_posts_in_str(posts: list):
    result_list = []
    for post in posts:
        result_list.append(json.dumps(post))
    result = '\n'.join(result_list)
    return result


class ServiceHandler(BaseHTTPRequestHandler):

    def _set_headers(self, response_code: int):
        self.send_response(response_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        (is_valid_url, unique_id) = check_url(self.path, "^/posts/([a-z0-9]+)?/?$", True)
        if is_valid_url:
            posts = get_posts()
            if unique_id is None:
                posts_str = convert_posts_in_str(posts)
                self._set_headers(200)
                self.wfile.write(posts_str.encode('utf-8'))
            else:
                elem = next((post for post in posts if post["unique_id"] == unique_id), None)
                if elem is not None:
                    self._set_headers(200)
                    self.wfile.write(str(json.dumps(elem)).encode('utf-8'))
                else:
                    self._set_headers(404)
        else:
            self._set_headers(400)

    def do_POST(self):
        (is_valid_url, unique_id) = check_url(self.path,"^/posts/$", False)
        if is_valid_url:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_json = json.loads(post_data)
            now: str = datetime.now().strftime("%Y%m%d")
            file_name = f'reddit-{now}.txt'
            if os.path.exists(file_name):
                if os.path.getsize(file_name) > 0:
                    posts = get_posts()
                    if post_json['unique_id'] in (post["unique_id"] for post in posts):
                        self._set_headers(405)
                    else:
                        with open("reddit-" + now + ".txt", "a") as file:
                            file.write('\n' + json.dumps(post_json))
                        with open("reddit-" + now + ".txt", "r") as file:
                            count = sum(1 for _ in file)
                else:
                    with open("reddit-" + now + ".txt", "a") as file:
                        file.write(json.dumps(post_json))
                    with open("reddit-" + now + ".txt", "r") as file:
                        count = sum(1 for _ in file)
            else:
                with open("reddit-" + now + ".txt", "w") as file:
                    file.write(json.dumps(post_json))
                with open("reddit-" + now + ".txt", "r") as file:
                    count = sum(1 for _ in file)
            self._set_headers(201)
            post_id = post_json["unique_id"]
            response = {post_id: count}
            self.wfile.write(str(json.dumps(response)).encode('utf-8'))
        else:
            self._set_headers(400)

    def do_PUT(self):
        (is_valid_url, unique_id) = check_url(self.path,"^/posts/([a-z0-9]+)/?$", True)
        if is_valid_url:
            posts = get_posts()
            elem = next((post for post in posts if post["unique_id"] == unique_id), None)
            if elem is not None:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                post_json = json.loads(post_data)
                if all(key in elem for key in post_json):
                    elem.update(post_json)
                    overwrite_file(posts)
                    self._set_headers(200)
                else:
                    self._set_headers(405)
            else:
                self._set_headers(404)
        else:
            self._set_headers(400)

    def do_DELETE(self):
        (is_valid_url, unique_id) = check_url(self.path,"^/posts/([a-z0-9]+)/?$", True)
        if is_valid_url:
            posts = get_posts()
            elem = next((post for post in posts if post["unique_id"] == unique_id), None)
            if elem is not None:
                posts.remove(elem)
                overwrite_file(posts)
                self._set_headers(200)
            else:
                self._set_headers(404)
        else:
            self._set_headers(400)


# Server Initialization
server = HTTPServer(('localhost', 8087), ServiceHandler)
server.serve_forever()
