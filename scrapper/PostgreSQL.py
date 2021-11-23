from psycopg2 import OperationalError, connect

from config import db_name, db_user, db_password, db_host, db_port


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    cursor = None
    try:
        connection = connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        connection.autocommit = True
        print("Connection to PostgreSQL DB successful")
        cursor = connection.cursor()
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection, cursor


def execute_query(query):
    try:
        cursor.execute(query)
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_read_query(query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# Будущий Init класса
(connection, cursor) = create_connection(db_name, db_user, db_password, db_host, db_port)

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

execute_query(create_users_table)
print("users_table created")
execute_query(create_posts_table)
print("posts_table created")


def post_method(data_to_posts, data_to_users):

    insert_query_users = (f"INSERT INTO users (user_name, post_karma, comment_karma, user_karma, user_cake_day) VALUES {data_to_users}")
    insert_query_posts = (f"INSERT INTO posts (unique_id, post_url, user_name, post_date, number_of_comments, number_of_votes) VALUES {data_to_posts}")

    select_user_name = f"SELECT user_name FROM users WHERE user_name = '{data_to_users[0]}'"
    user: list = execute_read_query(select_user_name)
    if not user:
        execute_query(insert_query_users)
    else:
        # Можно добавить обновление кармы и кармы коментов пользователя
        pass

    execute_query(insert_query_posts)


def get_method(**kwargs):

    GET = """SELECT posts.*, post_karma, comment_karma, user_karma, user_cake_day
            FROM posts
            INNER JOIN users
            ON posts.user_name = users.user_name;"""
    return execute_read_query(GET)


def put_method(**kwargs):
    pass


def delete_method(unique_id):
    delete_comment = f"DELETE FROM posts WHERE unique_id = {unique_id}"
    return execute_query(delete_comment)






