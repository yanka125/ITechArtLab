import pymongo

from config import mongo_uri, mongo_db_name


class Database(object):

    def __init__(self):
        try:
            client = pymongo.MongoClient(mongo_uri)
            self.mydb = client[mongo_db_name]
            print("Connection to MongoDB successful")
            # Create posts and users collections
            self.mydb["posts"].drop()
            self.posts_collection = self.mydb["posts"]
            self.mydb["users"].drop()
            self.users_collection = self.mydb["users"]
            print("users collection created")
            print("posts collection created")
        except Exception as e:
            print(f"The error '{e}' occurred")

    def get_from_database(self, unique_id=None):
        """Function to get data from database.

        :param unique_id: unique post ID
        :type unique_id: str
        :return: all data from database
        :rtype: list[tuple]
        """
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
                          "user_cake_day": "$user.user_cake_day"}}]

        database_data = []
        if unique_id is not None:
            match = {'$match': {'_id': f"{unique_id}"}}
            pipeline.append(match)

        for doc in (self.posts_collection.aggregate(pipeline)):
            database_data.append(tuple(doc.values()))

        return database_data

    def write_to_database(self, data_to_posts, data_to_users):
        """Function to write data to the database.

        :param data_to_posts: data to write to posts collection
        :type data_to_posts: tuple
        :param data_to_users: data to write to users collection
        :type data_to_users: tuple
        """
        insert_user = {
            "user_name": data_to_users[0],
            "post_karma": data_to_users[1],
            "comment_karma": data_to_users[2],
            "user_karma": data_to_users[3],
            "user_cake_day": data_to_users[4],
        }
        insert_post = {
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
        self.posts_collection.insert_one(insert_post)

    def update_database(self, data_to_users, user_name, data_to_posts, unique_id):
        """Function to update data in database.

        :param data_to_users: updated data to users collection
        :type data_to_users: dict
        :param user_name: user name
        :type user_name: str
        :param data_to_posts: updated data to posts collection
        :type data_to_posts: dict
        :param unique_id: unique post ID
        :type unique_id: str
        """
        self.posts_collection.update_one(
            {"_id": f"{unique_id}"},
            {"$set": data_to_posts
             })
        self.users_collection.update_one(
            {"user_name": f"{user_name}"},
            {"$set": data_to_users
             })

    def delete_from_database(self, unique_id):
        """Function to delete data from database.

        :param unique_id: unique post ID
        :type unique_id: str
        """
        delete_comment = {'_id': f"{unique_id}"}
        self.posts_collection.delete_one(delete_comment)
