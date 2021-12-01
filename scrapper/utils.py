import json
import logging
import re
from typing import List, Tuple, Dict, Union

USER_FIELDS = ["post_karma", "comment_karma", "user_karma", "user_cake_day"]
POST_FIELDS = ["post_url", "post_date", "number_of_comments", "number_of_votes"]

USER_PK = "user_name"
POST_PK = "unique_id"


def get_logger(format, level):
    """Function to configure the logger.

    :return: logger instance
    """
    logging.basicConfig(
        level=level,
        format=format,
    )
    logger = logging.getLogger(__name__)
    return logger


def split_data(data: Dict[str, Union[str, int]]):
    """Split data for collections / tables.

    :param data: all post data
    :return: data to users and posts collections / tables
    """
    data_to_users = dict((k, data[k]) for k in USER_FIELDS)
    data_to_posts = dict((k, data[k]) for k in POST_FIELDS)
    return data_to_users, data_to_posts


def convert_posts_to_dict(database_data: List[Tuple]):
    """Convert post data into list of dictionaries.

    :param database_data: row database data
    :return: all post data
    """
    result_list: List[Dict[str, Union[str, int]]] = []
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


def concat_posts_to_str(posts: List[Dict[str, Union[str, int]]]):
    """Function to convert list of dictionaries with post data
    to list of json strings.

    :param posts: post data
    :return: post data concatenated in string
    """
    result_list: List = []
    for post in posts:
        result_list.append(json.dumps(post))
    result: str = '\n'.join(result_list)
    return result


def check_url(path: str, pattern: str, extract_id: bool):
    """Function to check validity of url path by given regex pattern
    and extract unique_id if it exists in request.

    :param path: resource path from url
    :param pattern: regex pattern
    :param extract_id: flag to check if unique_id should be extracted
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
