from psycopg2 import OperationalError, connect

from config import db_name, db_user, db_password, db_host, db_port


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
                self.cursor = self.connection.cursor()
                self.create_tables()
            except OperationalError as e:
                print(f"The error '{e}' occurred")
        else:
            print("Connection established")

    def execute_query(self, query):
        """Function to send a query to the database.

        :param query: database query
        :type query: str
        """
        try:
            self.cursor.execute(query)
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query):
        """Function to send a query to the database. Return data from database.

        :param query: database query
        :type query: str
        :return: data from database
        :rtype: list
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def create_tables(self):
        """Function to create database tables."""
        create_users_table = """
        DROP TABLE IF EXISTS users CASCADE;
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
        DROP TABLE IF EXISTS posts CASCADE;
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
        self.execute_query(create_users_table)
        print("users_table created")
        self.execute_query(create_posts_table)
        print("posts_table created")

    def get_from_database(self, unique_id=None):
        """Function to get data from database.

        :param unique_id: unique post ID
        :type unique_id: str
        :return: all data from database
        :rtype: list[tuple]
        """
        get_query = """SELECT posts.*, post_karma, comment_karma, user_karma, user_cake_day
                FROM posts
                INNER JOIN users
                ON posts.user_name = users.user_name"""
        if unique_id is not None:
            get_query = get_query + f" WHERE unique_id = '{unique_id}';"
        return self.execute_read_query(get_query)

    def write_to_database(self, data_to_posts, data_to_users):
        """Function to write data to the database.

        :param data_to_posts: data to write to posts table
        :type data_to_posts: tuple
        :param data_to_users: data to write to users table
        :type data_to_users: tuple
        """
        insert_query_users = (
            f"INSERT INTO users (user_name, post_karma, comment_karma, user_karma, user_cake_day) VALUES {data_to_users}"
        )
        insert_query_posts = (
            f"INSERT INTO posts (unique_id, post_url, user_name, post_date, number_of_comments, number_of_votes) VALUES {data_to_posts}"
        )
        select_user_name = f"SELECT user_name FROM users WHERE user_name = '{data_to_users[0]}'"
        user: list = self.execute_read_query(select_user_name)

        # If user is not found in database, add user
        if not user:
            self.execute_query(insert_query_users)
        self.execute_query(insert_query_posts)

    def update_database(self, data_to_users, user_name, data_to_posts, unique_id):
        """Function to update data in database.

        :param data_to_users: updated data to users table
        :type data_to_users: tuple
        :param user_name: user name
        :type user_name: str
        :param data_to_posts: updated data to posts table
        :type data_to_posts: tuple
        :param unique_id: unique post ID
        :type unique_id: str
        """
        post_fields = str(tuple(data_to_posts.keys())).replace('\'', '')
        user_fields = str(tuple(data_to_users.keys())).replace('\'', '')
        post_values = tuple(data_to_posts.values())
        user_values = tuple(data_to_users.values())

        update_query_user = f"UPDATE users SET {user_fields} = {user_values} WHERE user_name = '{user_name}';"
        update_query_post = f"UPDATE posts SET {post_fields} = {post_values} WHERE unique_id = '{unique_id}';"

        self.execute_query(update_query_user)
        self.execute_query(update_query_post)

    def delete_from_database(self, unique_id):
        """Function to delete data from database.

        :param unique_id: unique post ID
        :type unique_id: str
        """
        delete_query = f"DELETE FROM posts WHERE unique_id = '{unique_id}'"
        self.execute_query(delete_query)
