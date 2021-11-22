import psycopg2


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def main(post_data):
    connection = create_connection(
        "Scrapper", "postgres", "scrapper", "127.0.0.1", "5432"
    )
    # post_data = ("24ccdd3d493611ec9cd0bc5ff4f0ce51", "https://www.reddit.com/r/MadeMeSmile/comments/qkq3a2/my_kid_was_a_little_sad_after_not_seeing_any/",
    #         "Atillion", "18 days ago", 1300, 177000, 57683, 89010, 192660, "October 31, 2015")
    insert_query = (
        f"INSERT INTO test (unique_id, post_url, user_name, post_date, number_of_comments,"
        f"number_of_votes, post_karma, comment_karma, user_karma, user_cake_day) VALUES {post_data}"
    )
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(insert_query, post_data)

