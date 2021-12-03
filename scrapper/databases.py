import logging
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Union

import pymongo
from psycopg2 import connect, OperationalError

from utils import split_data, USER_PK, get_logger

# Initializes the logger
logger = get_logger("%(asctime)s - %(levelname)s - %(message)s", logging.INFO)


class DatabaseHandler(ABC):
    @abstractmethod
    def get_from_database(self, unique_id: str = None):
        """Function to get data from database.

        :param unique_id: unique post ID
        :return: all data from database
        :rtype: List[Tuple]
        """
        pass

    @abstractmethod
    def write_to_database(self, data_to_posts: Tuple, data_to_users: Tuple):
        """Function to write data to the database.

        :param data_to_posts: data to write to posts collection
        :param data_to_users: data to write to users collection
        """
        pass

    @abstractmethod
    def update_database(self, data: Dict[str, Union[str, int]],
                        unique_id: str):
        """Function to update data in database.

        :param data: data to update
        :param unique_id: unique post ID
        """
        pass

    @abstractmethod
    def delete_from_database(self, unique_id: str):
        """Function to delete data from database.

        :param unique_id: unique post ID
        """
        pass


class MongoDB(DatabaseHandler):
    def __init__(self, mongo_uri: str, mongo_db_name: str):
        try:
            client = pymongo.MongoClient(mongo_uri)
            self.db = client[mongo_db_name]
            logger.info("Connection to MongoDB successful")
            # Create posts and users collections
            self.db["posts"].drop()
            self.posts_collection = self.db["posts"]
            logger.info("posts collection created")
            self.db["users"].drop()
            self.users_collection = self.db["users"]
            logger.info("users collection created")
        except Exception as _ex:
            logger.error("Failed to initialize collections")
            logger.error(_ex)

    def get_from_database(self, unique_id: str = None):
        pipeline = [{'$lookup':
                         {'from': 'users',
                          'localField': 'user_name',
                          'foreignField': 'user_name',
                          'as': 'user'}},
                    {'$unwind': '$user'},
                    {'$project':
                         {'_id': 1,
                          'post_url': 1,
                          "user_name": 1,
                          "post_date": 1,
                          "number_of_comments": 1,
                          "number_of_votes": 1,
                          "post_karma": "$user.post_karma",
                          "comment_karma": "$user.comment_karma",
                          "user_karma": "$user.user_karma",
                          "user_cake_day": "$user.user_cake_day"}
                     }]

        database_data = []
        if unique_id:
            match = {'$match': {'_id': f"{unique_id}"}}
            pipeline.append(match)

        for doc in (self.posts_collection.aggregate(pipeline)):
            database_data.append(tuple(doc.values()))

        return database_data

    def write_to_database(self, data_to_posts: Tuple, data_to_users: Tuple):
        insert_user: Dict[str, Union[str, int]] = {
            "user_name": data_to_users[0],
            "post_karma": data_to_users[1],
            "comment_karma": data_to_users[2],
            "user_karma": data_to_users[3],
            "user_cake_day": data_to_users[4],
        }
        insert_post: Dict[str, Union[str, int]] = {
            "_id": data_to_posts[0],
            "post_url": data_to_posts[1],
            "user_name": data_to_posts[2],
            "post_date": data_to_posts[3],
            "number_of_comments": data_to_posts[4],
            "number_of_votes": data_to_posts[5],
        }
        user_name = self.users_collection.find_one({"user_name": f"{data_to_users[0]}"})
        # If user is not found in database, add user
        if not user_name:
            self.users_collection.insert_one(insert_user)
        # Add post to collection
        self.posts_collection.insert_one(insert_post)

    def update_database(self, data: Dict[str, Union[str, int]], unique_id: str):
        (data_to_users, data_to_posts) = split_data(data)
        user_name = data[USER_PK]
        self.posts_collection.update_one(
            {"_id": f"{unique_id}"},
            {"$set": data_to_posts}
        )
        self.users_collection.update_one(
            {"user_name": f"{user_name}"},
            {"$set": data_to_users}
        )

    def delete_from_database(self, unique_id: str):
        delete_comment = {'_id': f"{unique_id}"}
        self.posts_collection.delete_one(delete_comment)


class PostgreSQL(DatabaseHandler):
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self._create_tables()

    def connection(self):
        """Function to connect to database and open a cursor"""
        try:
            connection = connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
            )
            connection.autocommit = True
            logger.info("Connection to PostgreSQL successful")
            return connection
        except OperationalError as _ex:
            logger.error(f"Failed to initialize connection: {_ex}")

    def get_from_database(self, unique_id: str = None):
        get_query = """SELECT posts.*, post_karma, comment_karma, user_karma, user_cake_day
                FROM posts
                INNER JOIN users
                ON posts.user_name = users.user_name"""
        if unique_id:
            get_query = get_query + f" WHERE unique_id = '{unique_id}';"
        return self._execute_read_query(get_query)

    def write_to_database(self, data_to_posts: Tuple, data_to_users: Tuple):
        insert_query_users = (
            f"INSERT INTO users (user_name, post_karma, comment_karma, user_karma, user_cake_day) VALUES {data_to_users}"
        )
        insert_query_posts = (
            f"INSERT INTO posts (unique_id, post_url, user_name, post_date, number_of_comments, number_of_votes) VALUES {data_to_posts}"
        )
        select_user_name = f"SELECT user_name FROM users WHERE user_name = '{data_to_users[0]}'"
        user: list = self._execute_read_query(select_user_name)

        # If user is not found in database, add user
        if not user:
            self._execute_query(insert_query_users)
        self._execute_query(insert_query_posts)

    def update_database(self, data: Dict[str, Union[str, int]], unique_id: str):
        (data_to_users, data_to_posts) = split_data(data)
        user_name = data[USER_PK]

        post_fields = str(tuple(data_to_posts.keys())).replace('\'', '')
        user_fields = str(tuple(data_to_users.keys())).replace('\'', '')
        post_values = tuple(data_to_posts.values())
        user_values = tuple(data_to_users.values())

        update_query_user = f"UPDATE users SET {user_fields} = {user_values} WHERE user_name = '{user_name}';"
        update_query_post = f"UPDATE posts SET {post_fields} = {post_values} WHERE unique_id = '{unique_id}';"

        self._execute_query(update_query_user)
        self._execute_query(update_query_post)

    def delete_from_database(self, unique_id: str):
        delete_query = f"DELETE FROM posts WHERE unique_id = '{unique_id}'"
        self._execute_query(delete_query)

    def _execute_query(self, query: str):
        """Function to send a query to the database.

        :param query: database query
        """
        with self.connection() as conn, conn.cursor() as cur:
            cur.execute(query)
        conn.close()

    def _execute_read_query(self, query: str):
        """Function to send a query to the database. Return data from database.

        :param query: database query
        :return: data from database
        :rtype: list
        """
        with self.connection() as conn, conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
        conn.close()
        return result

    def _create_tables(self):
        """Function to create database tables."""
        create_users_table = """
        TRUNCATE users CASCADE;
        CREATE TABLE IF NOT EXISTS users (
          user_name varchar(50), 
          post_karma INTEGER NOT NULL,
          comment_karma INTEGER NOT NULL,
          user_karma INTEGER NOT NULL,
          user_cake_day varchar(50) NOT NULL,
          PRIMARY KEY(user_name)
        )
        """
        create_posts_table = """
        TRUNCATE posts CASCADE;
        CREATE TABLE IF NOT EXISTS posts (
          unique_id char(32), 
          post_url varchar(150) NOT NULL,
          user_name varchar(50) NOT NULL,
          post_date varchar(20) NOT NULL,
          number_of_comments INTEGER NOT NULL,
          number_of_votes INTEGER NOT NULL,
          PRIMARY KEY(unique_id),
          FOREIGN KEY(user_name) 
          REFERENCES users(user_name)
          ON DELETE CASCADE
          ON UPDATE CASCADE
        )
        """
        self._execute_query(create_users_table)
        logger.info("users_table created")
        self._execute_query(create_posts_table)
        logger.info("posts_table created")
